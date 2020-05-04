import pytest

@pytest.fixture
def super_user(db, django_user_model):
    return django_user_model.objects.create_superuser(
        email='beta@gmail.com', first_name='beta', last_name="beta", password="12345678",)

@pytest.fixture
def regular_user(db, django_user_model):
    return django_user_model.objects.create_user(
        email='alfa@gmail.com', first_name='alfa', last_name="alfa", password="12345678",)
