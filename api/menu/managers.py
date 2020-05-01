from django.apps import apps
from django.db.models import Manager, Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.utils.timezone import localdate


class MenuManager(Manager):
    """
    Custom Menu Manager.
    """

    def create_menu(self, **model_arguments):
        available_date = model_arguments.get('available_date')

        self.model.objects.check_menu_at_date(available_date)
        
        options = model_arguments.pop('options')

        menu = self.model.objects.create(**model_arguments)

        if options:
            Option = apps.get_model('menu', 'Option')
            options = [Option(**{**option, 'menu': menu})
                       for option in options]
            Option.objects.bulk_create(options)

        return menu

    def is_editable(self, pk: str, raise_exception: bool = True) -> bool:
        """[Determines whether or not the stated object is available to be edited]

        Arguments:
            pk {[str]} -- [The Menu's ID over which the validation is gonna be performed ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [State that the current object shouldn't be updated at this moment]
        """
        model = self.model.objects.get(pk=pk)
        return model.is_editable(raise_exception)

    def has_ordered(self, menu, user, raise_exception: bool = True) -> bool:
        """[Determines whether or not a user has already ordered in a given menu]

        Arguments:
            menu {[object]} -- [The Menu's object to search for ]
            user {[object]} -- [The User's object to search for ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that the current user has already ordered an option for this menu]
        """
        try:
            self.model.objects.filter(Q(options__menu=menu) & Q(
                options__orders__user=user)).get()
        except ObjectDoesNotExist:
            return False
        else:
            if raise_exception:
                raise ValidationError(
                    {'detail': f'You has already placed an order in this menu'})
            else:
                return True

    def get_orders(self, pk) -> bool:
        """[Determines whether or not a user has already ordered in a given menu]

        Arguments:
            menu {[object]} -- [The Menu's object to search for ]
            user {[object]} -- [The User's object to search for ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that the current user has already ordered an option for this menu]
        """
        Order = apps.get_model('orders', 'Order')
        return Order.objects.filter(Q(option__menu_id=pk))

    def get_available(self) -> bool:
        """
        Returns the menu available for today
        """
        try:
            return self.model.objects.filter(available_date=localdate()).get()
        except ObjectDoesNotExist:
            return None            


    def check_menu_at_date(self, date, consultant_id=None, raise_exception: bool = True) -> bool:
        """[Determines whether or not already exist a menu in the stated date ]

        Arguments:
            date {[date]} -- [The date of the menu to search for]
            consultant_id {[str]} -- [Forces the method to return False if the found menu id is equal than consultant id]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that there is already a menu in the stated date]
        """
        try:
            menu = self.model.objects.get(available_date=date)
        except ObjectDoesNotExist:
            return False
        else:
            if menu.id == consultant_id:
                return False
            if raise_exception:
                raise ValidationError(
                    {'detail': f'There is already a menu created at {date}'})
            else:
                return True


class OptionManager(Manager):
    """
    Custom Option Manager.
    """

    def check_duplicated(self, menu_pk: str, name: str, raise_exception: bool = True) -> bool:
        """[Determines if already exists a duplicated]

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
