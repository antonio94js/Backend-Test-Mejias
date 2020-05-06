import pytest
import json
from django.urls import reverse
from api.menu.v1.views import MenuViewSet, OptionViewSet, PublicMenuViewSet
from api.menu.models import Menu, Option
from datetime import date

@pytest.mark.urls('api.menu.urls')
@pytest.mark.django_db
class TestMenuViewSet:
    def test_create(self, auth_rf, mocker, super_user, create_menu, menu_mock):
        """
        Should return status code 201 and call place_order method through serializers
        """
        url = reverse('menu-list')
        menu = create_menu()
        request = auth_rf.post(super_user, url, menu_mock, format='json')

        mocker.patch.object(Menu.objects, 'create_menu', return_value=menu)
        response = MenuViewSet.as_view({'post': 'create'})(request).render()

        content = json.loads(response.content)

        assert response.status_code == 201
        assert 'id' in content

        Menu.objects.create_menu.assert_called_once()

    def test_list(self, auth_rf, mocker, super_user, create_menu):
        """
        Should return status code 200 and filter the response by the appropriate user
        """
        create_menu()
        url = reverse('menu-list')
        request = auth_rf.get(super_user, url, format='json')

        mocker.spy(Menu.objects, 'filter')
        response = MenuViewSet.as_view({'get': 'list'})(request).render()

        content = json.loads(response.content)

        Menu.objects.filter.assert_called_once_with(user=super_user)
        assert response.status_code == 200
        assert len(content) == 1

    def test_update(self, auth_rf, mocker, super_user, menu_mock, create_menu):
        """
        Should return status code 200
        """
        menu = create_menu()
        pk = str(menu.id)
        url = reverse('menu-detail', kwargs={'pk': pk})
        request = auth_rf.put(super_user, url, menu_mock, format='json')

        mocker.spy(Menu.objects, 'filter')

        response = MenuViewSet.as_view({'put': 'update'})(request, pk=pk).render()

        content = json.loads(response.content)

        Menu.objects.filter.assert_called_once_with(user=super_user)

        assert response.status_code == 200
        assert content.get('id') == str(menu.id)
        assert content.get('name') ==  menu_mock.get('name')

    def test_retrieve(self, auth_rf, mocker, super_user, create_menu):
        """
        Should return status code 200 and filter the response by the appropriate user
        """
        menu = create_menu()
        pk = str(menu.id)
        url = reverse('menu-detail', kwargs={'pk': pk})
        request = auth_rf.get(super_user, url, format='json')

        mocker.spy(Menu.objects, 'filter')

        response = MenuViewSet.as_view({'get': 'retrieve'})(request, pk=pk).render()

        content = json.loads(response.content)

        Menu.objects.filter.assert_called_once_with(user=super_user)
        
        assert response.status_code == 200
        assert content.get('id') == str(menu.id)

    def test_get_orders(self, auth_rf, mocker, super_user, create_menu, create_order):
        """
        Should return status code 200 and call get_orders method
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        pk = str(menu.id)
        url = reverse('menu-get-orders', kwargs={'pk': pk})
        request = auth_rf.get(super_user, url, format='json')

        mocker.spy(Menu.objects, 'filter')
        mocker.patch.object(Menu.objects, 'get_orders', return_value=[create_order(option=option)])

        response = MenuViewSet.as_view({'get': 'get_orders'})(request, pk=pk).render()

        content = json.loads(response.content)

        Menu.objects.filter.assert_called_once_with(user=super_user)
        Menu.objects.get_orders.assert_called_once_with(pk=menu.id)
        
        assert response.status_code == 200
        assert len(content) == 1

@pytest.mark.urls('api.menu.urls')
@pytest.mark.django_db
class TestOptionViewSet:
    def test_create(self, auth_rf, mocker, super_user, create_menu, option_mock):
        """
        Should return status code 201 and call create_option method through serializers
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        menus_pk = str(option.id)
        url = reverse('option-list',  kwargs={'menus_pk': menus_pk})
        request = auth_rf.post(super_user, url, option_mock, format='json')

        mocker.patch.object(Option.objects, 'create_option', return_value=option)
        response = OptionViewSet.as_view({'post': 'create'})(request).render()

        content = json.loads(response.content)

        assert response.status_code == 201
        assert 'id' in content

        Option.objects.create_option.assert_called_once()

    def test_update(self, auth_rf, mocker, super_user, option_mock, create_menu):
        """
        Should return status code 200
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        menus_pk = str(menu.id)
        pk = str(option.id)

        url = reverse('option-detail', kwargs={'pk': pk, 'menus_pk': menus_pk})
        request = auth_rf.put(super_user, url, option_mock, format='json')

        response = OptionViewSet.as_view({'put': 'update'})(request,menus_pk=menus_pk, pk=pk).render()

        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('id') == str(option.id)
        assert content.get('name') ==  option_mock.get('name')

    def test_delete(self, auth_rf, mocker, super_user, create_menu):
        """
        Should return status code 204
        """
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        menus_pk = str(menu.id)
        pk = str(option.id)

        url = reverse('option-detail', kwargs={'pk': pk, 'menus_pk': menus_pk})
        request = auth_rf.delete(super_user, url, format='json')

        response = OptionViewSet.as_view({'delete': 'destroy'})(request,menus_pk=menus_pk, pk=pk).render()

        assert response.status_code == 204

@pytest.mark.urls('api.menu.urls')
@pytest.mark.django_db
class TestPublicMenuViewSet:
    
    def test_retrieve(self, api_rf, mocker, create_menu):
        """
        Should return status code 200 and retrieve the menu without authentication
        """
        menu = create_menu(available_date=date.today())
        pk = str(menu.id)
        url = reverse('daily-menu-detail', kwargs={'pk': pk})
        request = api_rf.get(url, format='json')

        response = PublicMenuViewSet.as_view({'get': 'retrieve'})(request, pk=pk).render()

        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('id') == str(menu.id)