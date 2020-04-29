from django.apps import apps
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


class MenuManager(models.Manager):
    """
    Custom Menu Manager.
    """

    def create_menu(self, **model_arguments):
        options = model_arguments.pop('options')
        available_date = model_arguments.get('available_date')
        # previous_menu = self.model.objects.get(available_date=available_date)
        # previous_menu = self.model.objects.filter(
        #     available_date=available_date)

        # if previous_menu:
        #     raise ValidationError(
        #         {'detail': f'You\'ve already created a menu for {available_date}'})

        self.model.objects.check_menu_at_date(available_date)

        menu = self.model.objects.create(**model_arguments)

        if options:
            Option = apps.get_model('menu', 'Option')
            options = [Option(**{**option, 'menu': menu})
                       for option in options]
            Option.objects.bulk_create(options)

        return menu

    def is_editable(self, pk: str, raise_exception: bool = True) -> bool:
        """[Determine whether or not the stated object is available to be edited]

        Arguments:
            pk {[str]} -- [The Menu's ID over which the validation is gonna be performed ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [State that the current object shouldn't be updated at this moment]
        """
        model = self.model.objects.get(pk=pk)
        return model.is_editable(raise_exception)

    def check_menu_at_date(self, date, consultant_id = None, raise_exception: bool = True) -> bool:
        """[Determine whether or not already exist a menu in the date stated]

        Arguments:
            date {[date]} -- [The date of the menu to search for]
            consultant_id {[str]} -- [Forces the method to return False if the found menu id is equal than consultant id]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that there is already a menu in the set date]
        """
        try:  
            menu = self.model.objects.get(available_date=date)
            if menu:
                if menu.id == consultant_id:
                    return False
                if raise_exception:
                    raise ValidationError(
                    {'detail': f'There is already a menu created at {date}'})
                else:
                    return True
        except ObjectDoesNotExist:
            return False

        
class OptionManager(models.Manager):
    """
    Custom Option Manager.
    """

    def check_duplicated(self, menu_pk: str, name: str, raise_exception: bool = True) -> bool:
        """[Determine if already exists a duplicated]

        Arguments:
            menu_pk {[str]} -- [The Menu's ID to search for ]
            name {[str]} -- [The Option's Name to search for ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: []
        """
        option = self.model.objects.filter(menu__pk=menu_pk, name=name)

        if option:
            if raise_exception:
                raise ValidationError(
                    {'detail': f'There is already an option with the name "{name}" in this menu'})
            else:
                return True  

        return False

   
