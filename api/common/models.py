from django.db import models
import uuid

class CommonModel(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    abstract = True