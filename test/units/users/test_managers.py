import pytest
from api.users.models import User
from datetime import datetime, timedelta, date
from uuid import uuid4

@pytest.mark.django_db
class TestUserManager:

    @pytest.mark.parametrize('method, assertions', [
        ('create_user', ['is_active']),
        ('create_superuser', ['is_active', 'is_staff', 'is_superuser']),
    ])
    def test_create_user(self, method, assertions):
        """
        Should create a new user properly
        """
        user_info = {
          'first_name': 'test',
          'last_name': 'test',
          'email': 'test@test.com',
          'password': '12345678'
        }
        
        user = getattr(User.objects, method)(**user_info)

        assert user.first_name == user_info['first_name']
        assert user.email == user_info['email']

        for prop in assertions:
           assert getattr(user, prop)

    @pytest.mark.parametrize('method, assertions', [
        ('create_user', ['is_active']),
        ('create_superuser', ['is_active', 'is_staff', 'is_superuser']),
    ])
    def test_create_user_missing_fields(self, method, assertions):
        """
        Should raise a ValueError if you miss required fields
        """
        user_info = {
          'last_name': 'test',
          'password': '12345678'
        }

        with pytest.raises(ValueError):
          getattr(User.objects, method)(None, None, **user_info)