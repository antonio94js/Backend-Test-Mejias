import pytest
from api.menu.permissions import IsPublicMenuAvailable, BelongsToMe, OptionBelongsToMenu
from datetime import date, timedelta
from uuid import uuid4

class TestIsPublicMenuAvailablePermission:

    permission = IsPublicMenuAvailable()

    @pytest.mark.parametrize('date, result', [
        (date.today(), True),
        (date.today() + timedelta(days=1), False)
    ])
    def test_has_object_permission(self, mocker, create_menu, date, result):
        """
        Should return True if the menu object is on its availability date, otherwise, False
        """
        menu = create_menu(available_date=date)
        request = mocker.MagicMock()
        view = mocker.MagicMock()

        assert self.permission.has_object_permission(request, view, menu) == result


class TestOptionBelongsToMenuPermission:

    permission = OptionBelongsToMenu()

    @pytest.mark.parametrize('method, menus_pk, result ', [
        ('PUT', None, True),
        ('DELETE', None, True),
        ('POST', None, True),
        ('GET', None, True),
        ('PUT', { 'menus_pk': uuid4() }, False),
        ('DELETE', { 'menus_pk': uuid4() }, False),
    ])
    def test_has_object_permission(self, mocker, create_menu, method, menus_pk, result):
        """
        Should return True if the HTTP method is PUT, DELETE and the object.menu.id is equal than the request menu id, otherwise, False
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        request = mocker.MagicMock(method=method)
        view = mocker.MagicMock(kwargs = menus_pk or { 'menus_pk':str(menu.id) })

        assert self.permission.has_object_permission(request, view, option) == result


class TestBelongsToMePermission:
  
    permission = BelongsToMe()

    @pytest.mark.parametrize('object_type ', ['menu', 'option'])
    @pytest.mark.parametrize('method ', ['PUT', 'DELETE', 'POST', 'GET'])
    def test_has_object_permission(self, mocker,create_menu, object_type, method):
        """
        Should return True if authenticated user is equal than the user who created the obj
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        request = mocker.MagicMock(user=menu.user, method=method)
        view = mocker.MagicMock(kwargs={})

        input_obj = menu if object_type == 'menu' else option
        assert self.permission.has_object_permission(request, view, input_obj) == True

    @pytest.mark.parametrize('object_type ', ['menu', 'option'])
    @pytest.mark.parametrize('method ', ['PUT', 'DELETE', 'POST'])
    def test_has_not_object_permission_(self, mocker, create_menu, regular_user, object_type, method):
        """
        Should return False if authenticated user is not equal than the user who created the obj
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        request = mocker.MagicMock(user=regular_user, method=method)
        view = mocker.MagicMock(kwargs={})

        input_obj = menu if object_type == 'menu' else option
        assert self.permission.has_object_permission(request, view, input_obj) == False
