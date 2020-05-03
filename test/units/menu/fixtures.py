import pytest
from typing import Optional
from api.menu.models import Menu, Option
from api.orders.models import Order
from datetime import date, timedelta
from ..helpers import get_future_day

@pytest.fixture
def create_menu(db, super_user):
    future_date = get_future_day()

    def menu_factory(user=super_user, name: Optional[str] = 'test', description: Optional[str] = 'test', available_date: Optional[date] = future_date, options: list = []) -> Menu:
        return Menu.objects.create_menu(user=user, name=name, description=description, available_date=available_date, options=options)
    return menu_factory


@pytest.fixture
def create_order(db, regular_user, create_menu):
    default_option = [{'name': 'test', 'description': 'test'}]

    def order_factory(additional_notes='test',  option: Optional[Option] = None, user=regular_user) -> Order:
        order_option = option if option else create_menu(options=default_option).options.first()
        return Order.objects.create(
            additional_notes=additional_notes, option=order_option, user=user)
    return order_factory
