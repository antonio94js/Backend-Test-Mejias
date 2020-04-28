from django.db import models
from django.conf import settings
from ..common.models import CommonModel
from .managers import MenuManager


class Menu(CommonModel):
    """
    Menu model class, in charge of representing the menu objects.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='menus')
    available_datetime = models.DateTimeField()
    name = models.CharField(max_length=30)
    description = models.TextField()

    objects = MenuManager()  # Setting the custom menu manager


class Option(CommonModel):
    """
    Option model class, in charge of representing the options inside a menu.
    """
    name = models.CharField(max_length=30)
    description = models.TextField()
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='options')
