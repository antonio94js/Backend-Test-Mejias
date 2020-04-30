from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.utils.timezone import localdate
from ..common.models import CommonModel
from .managers import MenuManager, OptionManager


class Menu(CommonModel):
    """
    Menu model class, in charge of representing the menu objects.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='menus')
    available_date = models.DateField()
    name = models.CharField(max_length=30)
    description = models.TextField()

    objects = MenuManager()  # Setting the custom menu manager

    def is_editable(self, raise_exception = True) -> bool:
        """[Determines whether or not the current model instance is available to be edited]

        Arguments:
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [State that the current object shouldn't be updated at this moment]
        """
        if (self.available_date == localdate()):
            if raise_exception:
                raise ValidationError(
                    {'detail': 'You cannot change the menu on the same release date'}, code=422)
            else:
                return False
        
        return True
    def is_available(self) -> bool:
        """
        Determines whether or not the current menu instance is on its launch date
        """
        # Reuses the is_editable behavior which is almost the same required for this method
        return not self.is_editable(False)


class Option(CommonModel):
    """
    Option model class, in charge of representing the options inside a menu.
    """
    name = models.CharField(max_length=30)
    description = models.TextField()
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='options')
    
    objects = OptionManager()  # Setting the custom menu manager

