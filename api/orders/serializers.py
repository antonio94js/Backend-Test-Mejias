from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from drf_dynamic_fields import DynamicFieldsMixin
from .models import Order
from ..menu.serializers import OptionNestedSerializer


class OrderSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    option_id = serializers.UUIDField(write_only=True)
    option = OptionNestedSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id','option_id', 'additional_notes', 'created_at', 'updated_at', 'option')

    def create(self, validated_data):
        option_id = validated_data.pop('option_id')
        user = validated_data.get('user')

        try: 
            Option = apps.get_model('menu.Option')
            option = Option.objects.get(pk=option_id)
        except ObjectDoesNotExist:
            raise NotFound({'detail': f'There\'s no any option with the id "{option_id}" in this menu'})
        else:
            if not option.menu.is_available():
                raise ValidationError({'detail': f'The menu "{option.menu.name}" is not available yet'})
            
            Menu = apps.get_model('menu.Menu')
            user = validated_data.get('user')

            if not Menu.objects.has_ordered(menu=option.menu, user=user):
                return Order.objects.create(option=option, **validated_data)

