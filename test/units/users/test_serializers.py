import pytest
from rest_framework.exceptions import ValidationError
from api.users.v1.serializers import UserSignUpSerializer
from api.users.models import User

user_mock = {
        'email': 'test@test.gmail.com',
        'first_name': 'test',
        'last_name': 'test',
        'password': '12345678'
    }

@pytest.mark.django_db
class TestUserSignUpSerializer:
  
    def test_valid_incoming_data(self):
        """
        Should return True when the incoming data to be deserialized is valid
        """
        serializer = UserSignUpSerializer(data=user_mock)

        assert serializer.is_valid()

    @pytest.mark.parametrize('input, context', [
        ({**user_mock, 'email': 123}, 'Invalid incoming data'),
        ({'first_name': 'test'}, 'Missing fields')
    ])
    def test_invalid_incoming_data(self, input, context):
        """
        Should raise ValidationError when the incoming data to be deserialized is invalid
        """

        serializer = UserSignUpSerializer(data=input)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
    
    def test_valid_serialized(self, regular_user):
        """
        Should return the respective serialized object
        """
        serializer = UserSignUpSerializer(regular_user)
        compare_attributes = ('id', 'email', 'first_name', 'last_name', 'created_at')

        assert isinstance(serializer.data, dict)

        for prop in compare_attributes:
            # just makes sure that every attribute exist
            assert prop in serializer.data

    def test_create(self, mocker, regular_user):
        """
        Should call create_user custom method instead of the predefined one (create)
        """
        serializer = UserSignUpSerializer(data=user_mock)

        mocker.patch.object(User.objects, 'create_user',return_value=regular_user)
        mocker.spy(User.objects, 'create')

        serializer.is_valid()
        serializer.save()

        User.objects.create_user.assert_called_once()
        User.objects.create.assert_not_called()
