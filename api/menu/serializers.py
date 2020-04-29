from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localdate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Menu, Option
import logging

logger = logging.getLogger("logger")


class OptionSerializer(serializers.ModelSerializer):
    # menu_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Option
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        menu_pk = validated_data.pop('menu_pk', None)

        try:
            menu = Menu.objects.get(id=menu_pk)
            menu.is_editable()
            Option.objects.check_duplicated(
                menu_pk=menu_pk, name=validated_data.get('name'))
        except ObjectDoesNotExist:
            raise ValidationError(
                {'detail': 'You tried to add an option to an non-existing menu'})
        except ValidationError as Error:
            raise ValidationError({'detail': Error.detail})
        else:
            return Option.objects.create(menu=menu, **validated_data)

    def update(self, instance, validated_data):
        menu_pk = validated_data.pop('menu_pk')

        if Menu.objects.is_editable(pk=menu_pk):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()

        return instance


class MenuSerializer(serializers.ModelSerializer):
    options = OptionSerializer(required=False, many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'available_date', 'options')

    def validate_available_date(self, value):
        """
        Validates the available_date field to be greater or equal than today
        """
        today = localdate()

        if value < today:
            raise ValidationError(
                {'detail': f'You cannot set a menu in the past, it must start at least since {today}'})

        return value

    def create(self, validated_data):
        # Calling the custom create_menu method
        return Menu.objects.create_menu(**validated_data)

    def update(self, instance, validated_data):
        if instance.is_editable():
            if 'available_date' in validated_data:
                Menu.objects.check_menu_at_date(
                    validated_data.get('available_date'), instance.id)

            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()

        return instance
