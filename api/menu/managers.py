from django.apps import apps
from django.db import models


class MenuManager(models.Manager):
    """
    Custom Menu Manager.
    """
    def create_menu(self, **model_arguments):
        options = model_arguments.pop('options')
        menu = self.model.objects.create(**model_arguments)
        if options:
            Option = apps.get_model('menu', 'Option')
            options = [Option(**{**option, 'menu': menu}) for option in options]
            Option.objects.bulk_create(options)

        return menu
