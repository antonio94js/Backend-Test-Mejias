import pytest
from typing import Optional
from rest_framework.test import APIRequestFactory, force_authenticate


class AuthAPIRequestFactory(APIRequestFactory):
    """
    Custom APIRequestFactory class which automatically authenticate the user against the created request
    """
    def get(self, user, *args, **kwargs):
        request = super().get(*args, **kwargs)
        force_authenticate(request, user=user)
        return request

    def post(self, user, *args, **kwargs):
        request = super().post(*args, **kwargs)
        force_authenticate(request, user=user)
        return request

    def put(self, user, *args, **kwargs):
        request = super().put(*args, **kwargs)
        force_authenticate(request, user=user)
        return request

    def delete(self, user, *args, **kwargs):
        request = super().delete(*args, **kwargs)
        force_authenticate(request, user=user)
        return request


@pytest.fixture
def super_user(db, django_user_model):
    return django_user_model.objects.create_superuser(
        email='beta@gmail.com', first_name='beta', last_name="beta", password="12345678",)


@pytest.fixture
def regular_user(db, django_user_model):
    return django_user_model.objects.create_user(
        email='alfa@gmail.com', first_name='alfa', last_name="alfa", password="12345678",)


@pytest.fixture
def api_rf():
    return APIRequestFactory()

@pytest.fixture
def auth_rf():
    return AuthAPIRequestFactory()


@pytest.fixture
def user_mock():
    return {
        'email': 'test@test.gmail.com',
        'first_name': 'test',
        'last_name': 'test',
        'password': '12345678'
    }
