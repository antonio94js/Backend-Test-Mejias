import pytest
from typing import Optional
from api.menu.models import Menu, Option
from api.orders.models import Order
from datetime import date, timedelta
from ..helpers import get_future_day

@pytest.fixture
def create_menu(db, super_user):
    future_date = get_future_day()
    default_option = [{'name': 'test', 'description': 'test'}]

    def menu_factory(user=super_user, name: Optional[str] = 'test', description: Optional[str] = 'test', available_date: Optional[date] = future_date, options: list = [],  use_default_option: Optional[bool] = False) -> Menu:
        options = options if not use_default_option else default_option
        return Menu.objects.create_menu(user=user, name=name, description=description, available_date=available_date, options=options)
    
    return menu_factory