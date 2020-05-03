import pytest
from rest_framework.exceptions import ValidationError
from api.menu.models import Menu
from datetime import date
from ..helpers import get_future_day


@pytest.mark.django_db
class TestMenuManager:
    @pytest.mark.parametrize('menu, options', [
        ({'name': 'test',
            'description': 'test',
            'available_date': date.today(), }, [{'name': 'test', 'description': 'test'}]),
        ({'name': 'test',
            'description': 'test',
            'available_date': date.today(), }, []),
    ])
    def test_create_menu(self, super_user, menu, options):
        """
        Should create a new menu properly either the options has been stated or not
        """
        menu_info = {
            **menu,
            'user': super_user,
            'options': options
        }
        menu = Menu.objects.create_menu(**menu_info)
        assert menu.name == menu_info['description']
        assert len(menu.options.all()) == len(options)

    def test_not_create_menu(self, super_user):
        """
        Should raise a ValidationError when a menu in the stated available_date already exist
        """
        menu_info = {
            'name': 'test',
            'description': 'test',
            'available_date': date.today(),
            'user': super_user,
            'options': []
        }
        with pytest.raises(ValidationError):
            Menu.objects.create_menu(**menu_info)  # First menu
            # Second menu with the same available_date
            Menu.objects.create_menu(**menu_info)

    def test_is_editable(self, create_menu):
        """
        Should return True is the menu queried by id is editable (out of its launch date)
        """
        menu = create_menu()  # By default this factory always create menu ahead of time
        assert Menu.objects.is_editable(menu.id)

    def test_is_not_editable(self, create_menu):
        """
        Should raise a ValidationError is the menu queried by id is not editable (it's on its launch date)
        """
        menu = create_menu(available_date=date.today())
        with pytest.raises(ValidationError):
            Menu.objects.is_editable(menu.id)

    def test_has_not_ordered(self, regular_user, create_menu):
        """
        Should return False is stated user hasn't placed any order in the menu
        """
        menu = create_menu()  # By default this factory always create menu ahead of time
        assert not Menu.objects.has_ordered(menu=menu, user=regular_user)

    def test_has_ordered(self, regular_user, create_menu, create_order):
        """
        Should raise a ValidationError by default if the user has already ordered in the stated menu
        """
        option = [{'name': 'test', 'description': 'test'}]
        menu = create_menu(available_date=date.today(), options=option)

        with pytest.raises(ValidationError):
            create_order(option=menu.options.first(),
                         user=regular_user)  # First order
            Menu.objects.has_ordered(menu=menu, user=regular_user)

    def test_get_orders(self, create_menu, create_order):
        """
        Should return a list with all the orders created for a menu
        """
        option = [{'name': 'test', 'description': 'test'}]
        menu = create_menu(available_date=date.today(), options=option)
        create_order(option=menu.options.first())

        result = Menu.objects.get_orders(pk=menu.id)
        assert len(result) == 1

    @pytest.mark.parametrize('available_date', [date.today(), get_future_day()])
    def test_get_available(self, create_menu, available_date):
        """
        Should return the today's menu if exist
        """
        create_menu(available_date=available_date)

        result = Menu.objects.get_available()

        if available_date == date.today():
            assert result
        else:
            assert not result

    @pytest.mark.parametrize('available_date, search_date,  set_consultant', [(date.today(), get_future_day(),  False), (get_future_day(), get_future_day(), True)])
    def test_check_at_date_not_exist(self, create_menu, available_date, search_date, set_consultant):
        """
        Should return False if there isn't any menu in the set date (it also should return False if the consultant menu id is equal than the searched menu)
        """
        menu = create_menu(available_date=available_date)

        result = Menu.objects.check_at_date(
            search_date, consultant_id=menu.id) if set_consultant else Menu.objects.check_at_date(search_date)

        assert not result

    def test_check_at_date_exist(self, create_menu):
        """
        Should raise a ValidationError by default if there's a menu in the set date
        """
        date = get_future_day(offset=30)
        create_menu(available_date=date)

        with pytest.raises(ValidationError):
            Menu.objects.check_at_date(date)

@pytest.mark.django_db
class TestOptionManager:
    @pytest.mark.parametrize('menu, options', [
        ({'name': 'test',
            'description': 'test',
            'available_date': date.today(), }, [{'name': 'test', 'description': 'test'}]),
        ({'name': 'test',
            'description': 'test',
            'available_date': date.today(), }, []),
    ])
    def test_create_menu(self, super_user, menu, options):
        """
        Should create a new menu properly either the options has been stated or not
        """
        menu_info = {
            **menu,
            'user': super_user,
            'options': options
        }
        menu = Menu.objects.create_menu(**menu_info)
        assert menu.name == menu_info['description']
        assert len(menu.options.all()) == len(options)

    def test_not_create_menu(self, super_user):
        """
        Should raise a ValidationError when a menu in the stated available_date already exist
        """
        menu_info = {
            'name': 'test',
            'description': 'test',
            'available_date': date.today(),
            'user': super_user,
            'options': []
        }
        with pytest.raises(ValidationError):
            Menu.objects.create_menu(**menu_info)  # First menu
            # Second menu with the same available_date
            Menu.objects.create_menu(**menu_info)

    def test_is_editable(self, create_menu):
        """
        Should return True is the menu queried by id is editable (out of its launch date)
        """
        menu = create_menu()  # By default this factory always create menu ahead of time
        assert Menu.objects.is_editable(menu.id)

    def test_is_not_editable(self, create_menu):
        """
        Should raise a ValidationError is the menu queried by id is not editable (it's on its launch date)
        """
        menu = create_menu(available_date=date.today())
        with pytest.raises(ValidationError):
            Menu.objects.is_editable(menu.id)

    def test_has_not_ordered(self, regular_user, create_menu):
        """
        Should return False is stated user hasn't placed any order in the menu
        """
        menu = create_menu()  # By default this factory always create menu ahead of time
        assert not Menu.objects.has_ordered(menu=menu, user=regular_user)

    def test_has_ordered(self, regular_user, create_menu, create_order):
        """
        Should raise a ValidationError by default if the user has already ordered in the stated menu
        """
        option = [{'name': 'test', 'description': 'test'}]
        menu = create_menu(available_date=date.today(), options=option)

        with pytest.raises(ValidationError):
            create_order(option=menu.options.first(),
                         user=regular_user)  # First order
            Menu.objects.has_ordered(menu=menu, user=regular_user)

    def test_get_orders(self, create_menu, create_order):
        """
        Should return a list with all the orders created for a menu
        """
        option = [{'name': 'test', 'description': 'test'}]
        menu = create_menu(available_date=date.today(), options=option)
        create_order(option=menu.options.first())

        result = Menu.objects.get_orders(pk=menu.id)
        assert len(result) == 1

    @pytest.mark.parametrize('available_date', [date.today(), get_future_day()])
    def test_get_available(self, create_menu, available_date):
        """
        Should return the today's menu if exist
        """
        create_menu(available_date=available_date)

        result = Menu.objects.get_available()

        if available_date == date.today():
            assert result
        else:
            assert not result

    @pytest.mark.parametrize('available_date, search_date,  set_consultant', [(date.today(), get_future_day(),  False), (get_future_day(), get_future_day(), True)])
    def test_check_at_date_not_exist(self, create_menu, available_date, search_date, set_consultant):
        """
        Should return False if there isn't any menu in the set date (it also should return False if the consultant menu id is equal than the searched menu)
        """
        menu = create_menu(available_date=available_date)

        result = Menu.objects.check_at_date(
            search_date, consultant_id=menu.id) if set_consultant else Menu.objects.check_at_date(search_date)

        assert not result

    def test_check_at_date_exist(self, create_menu):
        """
        Should raise a ValidationError by default if there's a menu in the set date
        """
        date = get_future_day(offset=30)
        create_menu(available_date=date)

        with pytest.raises(ValidationError):
            Menu.objects.check_at_date(date)
