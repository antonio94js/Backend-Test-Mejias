from django.apps import apps
from django.db.models import Manager, Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.utils.timezone import localdate
from ..common.utils import throwable

class MenuManager(Manager):
    """
    Custom Menu Manager.
    """

    def create_menu(self, **model_attributes):
        """
        Creates a new menu by applying all the proper validations
        """
        available_date = model_attributes.get('available_date')

        self.model.objects.check_at_date(available_date)
        
        options = model_attributes.pop('options')

        menu = self.model.objects.create(**model_attributes)

        if options:
            Option = apps.get_model('menu', 'Option')
            options = [Option(**{**option, 'menu': menu})
                       for option in options]
            Option.objects.bulk_create(options)

        return menu

    def is_editable(self, pk: str, raise_exception: bool = True) -> bool:
        """[Determines whether or not the stated menu by PK is available to be edited]

        Arguments:
            pk {[str]} -- [The Menu's ID over which the validation is gonna be applied]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that the stated menu mustn't be updated at this moment]
        """
        model = self.model.objects.get(pk=pk)
        return model.is_editable(raise_exception)

    @throwable(ValidationError, 'You has already placed an order in this menu')
    def has_ordered(self, menu, user, raise_exception: bool = True) -> bool:
        """[Determines whether or not a user has already placed an order in a given menu]

        Arguments:
            menu {[object]} -- [The Menu's object to search for ]
            user {[object]} -- [The User's object to search for ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that the current user has already placed an order for this menu]
        """
        try:
            self.model.objects.filter(Q(options__menu=menu) & Q(
                options__orders__user=user)).get()
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def get_orders(self, pk) -> bool:
        """[Gets the orders placed in a menu]

        Arguments:
            pk {[UUID]} -- [The Menu's ID to search for ]

        Returns:
            [QuerySet] -- [orders placed over the stated menu]
        """
        Order = apps.get_model('orders', 'Order')
        return Order.objects.filter(option__menu_id=pk)

    def get_available(self) -> bool:
        """
        Returns the menu available for today
        """
        try:
            return self.model.objects.filter(available_date=localdate()).get()
        except ObjectDoesNotExist:
            return None            

    @throwable(ValidationError, 'There is already a menu created on the set date')
    def check_at_date(self, date, consultant_id=None, raise_exception: bool = True) -> bool:
        """[Determines whether or not a menu in the stated date already exist]

        Arguments:
            date {[date]} -- [The date to search for]
            consultant_id {[str]} -- [Forces the method to return False if the found menu id is equal than the consultant menu id]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: [States that there is already a menu in the set date]
        """
        try:
            menu = self.model.objects.get(available_date=date)
        except ObjectDoesNotExist:
            return False
        else:
            return not menu.id == consultant_id


class OptionManager(Manager):
    """
    Custom Option Manager.
    """

    def create_option(self, **model_arguments) -> bool:
        """
        Creates a new option by applying all the proper validations
        """
        Menu = apps.get_model('menu', 'Menu')
        menu_pk = model_arguments.pop('menu_pk', None)

        try:
            menu = Menu.objects.get(id=menu_pk)
            menu.is_editable()
            self.model.objects.check_duplicated(
                menu_pk=menu_pk, name=model_arguments.get('name'))
        except ObjectDoesNotExist:
            raise ValidationError(
                {'detail': 'You tried to add an option to an non-existing menu'})
        except ValidationError as error:
            raise ValidationError({'detail': error.detail})
        else:
            return self.model.objects.create(menu=menu, **model_arguments)

    @throwable(ValidationError, 'There is already an option with the set name in this menu')
    def check_duplicated(self, menu_pk: str, name: str, raise_exception: bool = True) -> bool:
        """[Determines if a duplicated option already exists]

        Arguments:
            menu_pk {[str]} -- [The Menu's ID to search for ]
            name {[str]} -- [The Option's Name to search for ]
            raise_exception {[bool]} -- [Whether or not this method should raise an exception]

        Raises:
            ValidationError: []
        """
        option = self.model.objects.filter(menu__pk=menu_pk, name=name)

        return bool(option)
