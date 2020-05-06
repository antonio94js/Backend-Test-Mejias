from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_flex_fields import FlexFieldsModelSerializer
from ...menu.v1.serializers import OptionNestedSerializer
from ...users.v1.serializers import UserSignUpSerializer
from ..models import Order


class OrderSerializer(FlexFieldsModelSerializer):
    option_id = serializers.UUIDField(write_only=True)
    option = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    additional_notes = serializers.CharField(allow_blank=True)

    class Meta:
        model = Order
        fields = ('id','option_id', 'additional_notes', 'created_at', 'updated_at', 'option', 'user')
        expandable_fields = {
            'option': OptionNestedSerializer,
            'user': UserSignUpSerializer
        }

    def create(self, validated_data):
        return Order.objects.place_order( **validated_data)
