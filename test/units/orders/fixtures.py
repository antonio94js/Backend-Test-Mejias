
import pytest
from typing import Optional
from api.menu.models import Option
from api.orders.models import Order
from datetime import date, timedelta, datetime


@pytest.fixture
def create_order(db, regular_user, create_menu):
    def order_factory(additional_notes='test', option: Optional[Option] = None, user=regular_user) -> Order:
        order_option = option or create_menu(use_default_option=True).options.first()
        return Order.objects.create(
            additional_notes=additional_notes, option=order_option, user=user)

    return order_factory


@pytest.fixture
def set_on_time(mocker, monkeypatch):
    mock_date = mocker.patch('api.common.utils.datetime')
    mock_date.now.return_value = datetime.now() - timedelta(days=1)
    mock_date.side_effect = lambda *args, **kw: datetime(*args, **kw)

    monkeypatch.setenv('LIMIT_ORDER_HOUR',  str((datetime.now() + timedelta(hours=1)).hour))
