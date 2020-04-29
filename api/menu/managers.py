from django.apps import apps
from django.db import models
from rest_framework.exceptions import ValidationError


class MenuManager(models.Manager):
    """
    Custom Menu Manager.
    """

    def create_menu(self, **model_arguments):
        options = model_arguments.pop('options')
        available_date = model_arguments.get('available_date')
        previous_menu = self.model.objects.get(available_date=available_date)

        if previous_menu:
            raise ValidationError(
                {'detail': f'You\'ve already created a menu for {available_date}'})

        menu = self.model.objects.create(**model_arguments)

        if options:
            Option = apps.get_model('menu', 'Option')
            options = [Option(**{**option, 'menu': menu})
                       for option in options]
            Option.objects.bulk_create(options)

        return menu
    
    def is_editable(self, pk: str, raise_exception = True) -> bool:
        """[Define whether or not the current model is available]

        Arguments:
            pk {[str]} -- [The Menu's ID over which the validation is gonna be performed ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [State that the current object shouldn't be updated at this moment]
        """
        model = self.model.objects.get(pk=pk)
        return model.is_editable(raise_exception)
