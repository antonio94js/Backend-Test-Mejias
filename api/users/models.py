from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from ..common.models import CommonModel
import uuid

class User(AbstractUser, CommonModel):
    username = None  # Remove username field
    date_joined = None # Remove date_joined field
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email