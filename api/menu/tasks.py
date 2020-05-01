from __future__ import absolute_import, unicode_literals
import os
import logging
import asyncio
from slack import WebClient
from slack.errors import SlackApiError
from config.celery import app
from .models import Menu

logger = logging.getLogger("logger")

async def get_all_slack_user_list(client: WebClient, cursor: str = '') -> list:
    """[Recursive function responsible for getting all the users available inside a slack workspace regarding pagination]

    Keyword Arguments:
        client {WebClient} -- [The SlackClient instance])
        cursor {str} -- [cursor used for pagination] (default: {''})

    Returns:
        [list] -- [users list of the respective pagination set]
    """
    try:
        response = await client.users_list(cursor=cursor)

    except SlackApiError as e:
        logger.error(f"Got an error: {e.response['error']}")
        return []
    else:
        total_users = response.get("members", [])

        users = [{'id': user.get('id'), 'real_name': user.get('real_name')}
                 for user in total_users if not user.get('is_bot', False)]

        next_cursor = response["response_metadata"]["next_cursor"]

        if next_cursor:
            users += await get_all_slack_user_list(client, next_cursor)
            return users

        return users


async def create_slack_channels(client: WebClient) -> list:
    """[Create (or re-open) the private channels where the message are gonna be sent to]

    Arguments:
        client {WebClient} -- [The SlackClient instance]

    Returns:
        list -- [a list containing all the channels IDs]
    """
    async def open_channels(user):
        try:
            response = await client.conversations_open(users=user['id'])         
        except SlackApiError as e:
            logger.error(f"Got an error: {e.response['error']}")
            return None
        else:
            return response['channel']['id']
        
    users = await get_all_slack_user_list(client)
    open_channels = [open_channels(user=user) for user in users]

    # Starts all the HTTP requests concurrently in order to cut down on response times
    channels = await asyncio.gather(*open_channels)

    return channels


async def send_slack_message(text: str, client: WebClient) -> None:
    """[Send the today's menu to all the slack users available in the workspace through a direct bot message]

    Arguments:
        message {str} -- [The message to be sent]
        client {WebClient} -- [The SlackClient instance]
    """
    channels = await create_slack_channels(client)

    post_channels = [client.chat_postMessage(
        channel=channel, text=text) for channel in channels if channel]

    # Starts all the HTTP requests concurrently in order to cut down on response times
    await asyncio.gather(*post_channels)


@app.task()
def send_daily_menu():
    menu = Menu.objects.get_available()

    if menu:
        logger.info("There's a menu available for today :)")

        url = os.environ.get('PUBLIC_MENU_URL').format(menu.id)
        client = WebClient(token=os.environ.get('SLACK_TOKEN'), run_async=True)

        asyncio.run(send_slack_message(url, client))
    else:
        logger.warn("We don't have any menu available for today :(")
