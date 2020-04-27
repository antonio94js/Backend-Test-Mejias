from rest_framework import serializers
from .models import User
import logging
logger = logging.getLogger("logger")

class UserSignUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'first_name', 'last_name', 'password', 'created_at')
    extra_kwargs = {
      'password': { 'write_only': True }
    }

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user