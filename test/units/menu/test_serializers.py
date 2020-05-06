import pytest
from rest_framework.exceptions import ValidationError
from api.menu.v1.serializers import MenuSerializer, OptionSerializer
from api.menu.models import Menu, Option
from uuid import uuid4
from datetime import date, timedelta

@pytest.mark.django_db
class TestMenuSerializer:

    def test_valid_incoming_data(self, menu_mock):
        """
        Should return True when the incoming data to be deserialized is valid
        """
        serializer = MenuSerializer(data=menu_mock)

        assert serializer.is_valid()

    @pytest.mark.parametrize('input_data, context', [
        ({'name': date.today()}, 'Invalid incoming data'),
        ({'name': 'test'}, 'Missing fields'),
        ({'available_date': date.today() - timedelta(days=1)}, 'Invalid date in the past')
    ])
    def test_invalid_data(self, input_data, context, menu_mock):
        """
        Should raise a ValidationError when the input data to be deserialized is invalid.
        """
        input_data = {**menu_mock, **input_data } if context != 'Missing fields' else input_data

        serializer = MenuSerializer(data=input_data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_serialized(self, create_menu):
        """
        Should return the respective serialized object
        """
        menu = create_menu()
        serializer = MenuSerializer(menu)
        compare_attributes = ('id', 'name', 'description',
                              'available_date', 'options')

        assert isinstance(serializer.data, dict)

        for prop in compare_attributes:
            # just makes sure that every attribute exist
            assert prop in serializer.data

    def test_create(self, mocker, create_menu, menu_mock):
        """
        Should call create_menu custom method instead of the predefined one (create)
        """
        menu = create_menu()
        serializer = MenuSerializer(data=menu_mock)

        mocker.patch.object(Menu.objects, 'create_menu', return_value=menu)
        mocker.spy(Menu.objects, 'create')

        serializer.is_valid()
        serializer.save()

        Menu.objects.create_menu.assert_called_once()
        Menu.objects.create.assert_not_called()

    def test_update(self, mocker, create_menu, menu_mock):
        """
        Should call instance.save() method and update the instance 
        """

        menu = create_menu()
        serializer = MenuSerializer(menu, data=menu_mock)
        
        mocker.spy(menu, 'save')
        mocker.spy(menu, 'is_editable')
        mocker.patch.object(Menu.objects, 'check_at_date', return_value=False)

        serializer.is_valid()
        serializer.save()

        menu.refresh_from_db()

        menu.is_editable.assert_called_once()
        Menu.objects.check_at_date.assert_called_once_with(menu_mock.get('available_date'), menu.id)
        menu.save.assert_called_once()
        
        assert getattr(menu, 'name') == menu_mock.get('name')


@pytest.mark.django_db
class TestOptionSerializer:
 
    def test_valid_incoming_data(self, option_mock):
        """
        Should return True when the incoming data to be deserialized is valid
        """
        serializer = OptionSerializer(data=option_mock)

        assert serializer.is_valid()

    @pytest.mark.parametrize('input_data, context', [
        ({ 'name': date.today()}, 'Invalid incoming data'),
        ({'name': 'test'}, 'Missing fields')
    ])
    def test_invalid_data(self, input_data, context, option_mock):
        """
        Should raise a ValidationError when the input data to be deserialized is invalid.
        """
        input_data = {**option_mock, **input_data} if context != 'Missing fields' else input_data

        serializer = OptionSerializer(data=input_data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_valid_serialized(self, create_menu):
        """
        Should return the respective serialized object
        """
        menu = create_menu(use_default_option=True)
        serializer = OptionSerializer(menu.options.first())
        compare_attributes = ('id', 'name', 'description')

        assert isinstance(serializer.data, dict)

        for prop in compare_attributes:
            # just makes sure that every attribute exist
            assert prop in serializer.data

    def test_create(self, mocker, create_menu, option_mock):
        """
        Should call create_option custom method instead of the predefined one (create)
        """
        menu = create_menu(use_default_option=True)
        serializer = OptionSerializer(data=option_mock)

        mocker.patch.object(Option.objects, 'create_option',
                            return_value=menu.options.first())
        mocker.spy(Option.objects, 'create')

        serializer.is_valid()
        serializer.save()

        Option.objects.create_option.assert_called_once()
        Option.objects.create.assert_not_called()

    def test_update(self, mocker, create_menu, option_mock):
        """
        Should call instance.save() method and update the instance 
        """
        
        menu = create_menu(use_default_option=True)
        option = menu.options.first()
        menus_pk = menu.id

        serializer = OptionSerializer(option, data=option_mock)
        
        mocker.spy(option, 'save')
        mocker.patch.object(Menu.objects, 'is_editable', return_value=True)

        serializer.is_valid()
        serializer.save(menus_pk=menus_pk)

        option.refresh_from_db()

        Menu.objects.is_editable.assert_called_once_with(pk=menu.id)
        option.save.assert_called_once()

        assert getattr(option, 'name') == option_mock.get('name')
