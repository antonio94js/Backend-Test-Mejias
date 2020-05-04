from django.db.models import Manager
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from rest_framework.exceptions import ValidationError, NotFound
from ..common.utils import on_time 


class OrderManager(Manager):
    @on_time
    def place_order(self, **model_attributes):
        print('callinnng')
        """
        Place a new order for a given option and perform the respective validations
        """
        option_id = model_attributes.pop('option_id')

        try:
            Option = apps.get_model('menu.Option')
            option = Option.objects.get(pk=option_id)
        except ObjectDoesNotExist:
            raise NotFound(
                {'detail': f'There\'s no any option with the id "{option_id}" in this menu'})
        else:
            if not option.menu.is_available():
                raise ValidationError(
                    {'detail': f'The menu "{option.menu.name}" is not available'})

            Menu = apps.get_model('menu.Menu')
            user = model_attributes.get('user')

            if not Menu.objects.has_ordered(menu=option.menu, user=user):
                return self.model.objects.create(option=option, **model_attributes)