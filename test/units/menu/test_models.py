import pytest
from rest_framework.exceptions import ValidationError
from datetime import date

@pytest.mark.django_db
class TestMenuModel:
    def test_is_editable(self, create_menu):
        """
        Should return true is the menu is editable (out of its launch date)
        """
        menu = create_menu()
        assert menu.is_editable()

    def test_is_not_editable(self, create_menu):
        """
        Should raise a ValidationError if the menu not editable (it's on its launch date)
        """
        menu = create_menu(available_date=date.today())
        with pytest.raises(ValidationError):
            assert menu.is_editable()

    def test_is_available(self, create_menu):
        """
        Should return true is the menu is available (on its launch date)
        """
        menu = create_menu(available_date=date.today())
        assert menu.is_available()

    def test_is_not_available(self, create_menu):
        """
        Should return false if the menu not available yet
        """
        menu = create_menu() # By default this factory always create menu in the future
        assert not menu.is_available()

    def test_get_user(self, super_user, create_menu):
        """
        Should return the user who created the menu
        """
        menu = create_menu(user=super_user)
        assert menu.get_user().id == super_user.id

@pytest.mark.django_db
class TestOptionModel:
    def test_get_user(self, super_user, create_menu):
        """
        Should return the user who created the menu in which the option is set
        """
        options = [{ 'name': 'test', 'description': 'test' }]
        menu_with_options = create_menu(user=super_user, options=options)
        assert menu_with_options.options.first().get_user().id == super_user.id
