import pytest
from rest_framework.exceptions import ValidationError, NotFound
from api.orders.models import Order
from datetime import date
from uuid import uuid4


@pytest.mark.django_db
class TestOrderManager:
    base_order = {
        'additional_notes': 'test test',
    }

    def test_place_order(self, set_on_time, regular_user, create_menu):
        """
        Should place a new order if all the validations pass
        """

        menu = create_menu(use_default_option=True,
                           available_date=date.today())
        order_info = {
            **self.base_order,
            'user': regular_user,
            'option_id': menu.options.first().id
        }
        order = Order.objects.place_order(**order_info)
        assert order.additional_notes == order_info['additional_notes']
        assert order.user.id == regular_user.id

    def test_place_order_option_not_exist(self, set_on_time, regular_user, create_menu):
        """
        Should raise a ValidationError if the set option doesn't exist
        """
        option_id = uuid4()
        order_info = {
             **self.base_order,
            'user': regular_user,
            'option_id': option_id
        }

        with pytest.raises(NotFound):
            Order.objects.place_order(**order_info)

    def test_place_menu_not_available(self, set_on_time, regular_user, create_menu):
        """
        Should raise a ValidationError if the menu the option was created from is not available
        """
        menu = create_menu(use_default_option=True) # By default this factory creates menus in the future
        order_info = {
             **self.base_order,
            'user': regular_user,
            'option_id': menu.options.first().id
        }

        with pytest.raises(ValidationError):
            Order.objects.place_order(**order_info)

    def test_place_menu_already_order(self, set_on_time, regular_user, create_menu):
        """
        Should raise a ValidationError if the user has placed an order in this menu already
        """
        menu = create_menu(use_default_option=True,
                           available_date=date.today())
        order_info = {
             **self.base_order,
            'user': regular_user,
            'option_id': menu.options.first().id
        }

        with pytest.raises(ValidationError):
            Order.objects.place_order(**order_info) # Create the first order
            Order.objects.place_order(**order_info) # Try to create a second order with the same user
