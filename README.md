

- [Description](#description)
- [Project's Structure Folder](#project-s-structure-folder)
- [Environment Variables](#environment-variables)
- [Principal Dependencies](#principal-dependencies)
- [Install and Execution](#install-and-execution)
- [API Docs](#api-docs)
- [Tests Execution](#tests-execution)



## Description

Meal app which daily at 8:00 am send a slack notification through a slack bot with the today's menu, so that all the employees inside a slack workspace can be able to order their favorite meal option in just a few clicks.

## Technical approaches

This section is intended to summarize some tech decisions taken during this project development.

 - The core API is fully developed with Django using Django Rest Framework, therefore, the project doesn't use the classic monolith MVT approach which come by default with Django, instead, the final solution is a bit more oriented to a three-tier architecture approach having the API and frontend app decoupled between them (this mean that I'm not using the `Template` mechanism offered by Django). Despite all of that, the final frontend solution is still served through the Django server, but this last one needs to be compiled first.
 
 -  To handle async tasks/cron jobs this project leverages Celery's power in order to provide a more resilient solution.
 
 - The slack integration was made using the [Slack's recommended way for new apps](https://api.slack.com/authentication/quickstart#overview).


## Project's Structure Folder

| Folder | Description |
| -------- | -------- |
| `api` | This folder contains all the Django Apps used for creating the API Rest |
| `config` | This folder contains all the Django default and custom configurations |
| `docker` | This folder contains some scripts and subfolders which are gonna be useful when running the app with docker |
| `frontend` | This folder contains the whole client app which is gonna be compiled and served through Django server |
| `test` | This folder contains all the units test of the differents apps |

## Environment Variables

Down below you will find all the env vars which are needed to start the project.

| Variable | Description |
| -------- | -------- |
| `DEBUG` | Turns on and off the debug mode  |
| `SECRET_KEY` | Django secret_key  |
| `JWT_SECRET_KEY` | Secret used to sign the JWT |
| `SQL_ENGINE` | The SQL Database engine |
| `SQL_DATABASE` | The database name |
| `SQL_USER` | The database user |
| `SQL_PASSWORD` | The database password |
| `SQL_HOST` | The database host |
| `SQL_PORT` | The database port |
| `SLACK_TOKEN` | The slack token used for the bot in charge of sending the daily menu |
| `PUBLIC_MENU_URL` | This will be the URL sent through slack which the employee is gonna access to  |
| `REDIS_URI` | The Redis URI which is used by Celery as a message broker for async tasks and cron jobs |
| `LIMIT_ORDER_HOUR` | This var set the limit hour in which an employee can place an order |

**IMPORTANT:** 

The project comes with a `.env.example` at root, which has some default values to help you to get started, but remember setting your own `SLACK_TOKEN` and if you want to run this project fully locally remember setting `PUBLIC_MENU_URL` to `http://localhost:8000/menu/{}` otherwise it will be `https://nora.cornershop.io/menu/{}`

If you want to change the time limit the employees have to place an order you could get this done by changing the `LIMIT_ORDER_HOUR` var and if you want to change the time in which the slack notification is sent you should change [this value](https://github.com/antonio94js/Backend-Test-Mejias/blob/master/config/settings.py#L211
) in the code to the hour you need to.


## Principal Dependencies

| Dependency | Purpose |
| -------- | -------- |
| `Django` | Used to build the whole project |
| `djangorestframework` | Used to build all the API Rest |
| `celery` | Used to handle async tasks and cron jobs |
| `pytest` | Used to write all the unit tests |
| `redis` | Used to allow Celery to connect with the Redis server |
| `slackclient` | Used to communicate with the Slack Web API |
| `Django` | Used to build the whole project |
| `psycopg2-binary` | Used to connect with Postgres |

 ## App considerations

Regarding the initial requirements, these are the features this app come with:

**Regular users (employees):**

- Everyone can see the public today's menu, but just **regular logged-in users** can order
- Everyone can sign up as a regular user and sign in
- Every regular user can get into a dashboard in which they can see their previous orders

**Administrator (Nora):**

- Nora can sign in and get into a Menu management dashboard in which she can create new menus with different options and prices, edit those menus, and see who has placed orders on them.

## Install and Execution

### Previous steps

Previous to run this project, you should create a [new slack app](https://api.slack.com/authentication/basics) and get your [slack bot token.](https://api.slack.com/authentication/token-types#granular_bot) 

When creating the new slack app, as stated for them, you should grant some granular permissions, the permissions required for this project are [`users:read`](https://api.slack.com/scopes/users:read) [`  
channels:manage`](https://api.slack.com/scopes/channels:manage) [`groups:write`](https://api.slack.com/scopes/groups:write) [`im:write`](https://api.slack.com/scopes/im:write) [`mpim:write`](https://api.slack.com/scopes/mpim:write) [`  
chat:write`](https://api.slack.com/scopes/chat:write "Only for use with new Slack apps.")

Remember install this app in your workspace and get your **Bot User OAuth Access Token**


### Main process

To easily get this project up and running I recommend using [`docker-compose`](https://docs.docker.com/compose/) in order to spin up all the dependencies and boring stuff rather quickly.

*1. Firstly, you will need to clone this locally*

`git clone https://github.com/antonio94js/Backend-Test-Mejias.git`

`cd Backend-Test-Mejias`

 *2. Once inside the project's folder, you just need to run the following command:*

`docker-compose up`

*3. After all the ecosystem has been spun up, you should go inside the container :*

`docker-compose exec api bash` 

*4. Run the migrations:*

`dj migrate` 

or 

`python manage.py migrate`

*5. This app allows regular users (employees) to sign up, but the superuser (nora) must be created by running:*
 
 `dj createsuperuser` 

 or 

 `python manage.py createsuperuser`

*6. And start the Celery worker (you should re-run this command every time you restart the container):*
 
 `celery -A config worker -l info -B`

Now you can hit `http://localhost:8000` and see the application running :)

**Note:** If you make some chances to the env vars after the API container has been started, you could run 

`docker-compose up --force-recreate --no-deps -d api` 

to update the environment.

## API Docs

You can find the API Docs at the project root with the name `apidocs.yml` . This documentation was written using the Open API specs and Swagger, you can gaze the API properly by copy-paste the code [here](https://editor.swagger.io/). This doc contains a detailed explanation about what the API does, the responses and errors you may run into by consuming it

## Tests Execution

*1.  Go inside the container*

`docker-compose exec api bash`

*2.  Run the tests*

`pytest test/units`