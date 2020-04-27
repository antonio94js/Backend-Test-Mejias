from rest_framework import serializers
from .models import User
import logging
logger = logging.getLogger("logger")
logger.info("Whatever to log")

class UserSignUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'first_name', 'last_name', 'password', 'created_at')
    # fields = '__all__'
    extra_kwargs = {
      'password': { 'write_only': True }
    }

  def create(self, validated_data):
    logging.info(validated_data)
    logging.info("aqui choroooo")
    # User.
    user = User.objects.create_user(**validated_data)
    return user