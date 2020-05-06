from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localdate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Menu, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'name', 'description', 'price')

    def create(self, validated_data):
        return Option.objects.create_option(**validated_data)

    def update(self, instance, validated_data):
        menus_pk = validated_data.pop('menus_pk')

        if Menu.objects.is_editable(pk=menus_pk):
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
                {'detail': f'You cannot set a menu in the past, it must start at least from {today}'})

        return value

    def create(self, validated_data):
        # Calling the custom create_menu method
        return Menu.objects.create_menu(**validated_data)

    def update(self, instance, validated_data):

        if instance.is_editable():
            if 'options' in validated_data:
                del validated_data['options']
                
            if 'available_date' in validated_data:
                Menu.objects.check_at_date(
                    validated_data.get('available_date'), instance.id)

            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()

        return instance


class OptionNestedSerializer(OptionSerializer):

    class Meta(OptionSerializer.Meta):
        fields = OptionSerializer.Meta.fields + ('menu',)
        depth = 1