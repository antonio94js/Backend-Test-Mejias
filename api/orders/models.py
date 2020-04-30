from django.apps import apps
from django.conf import settings
from django.db import models
from ..common.models import CommonModel
from ..menu.models import Option

class Order(CommonModel):
  user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
  option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='orders')
  additional_notes = models.TextField()