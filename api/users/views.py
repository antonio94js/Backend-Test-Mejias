from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSignUpSerializer
from .models import User

class UserSignUpViewSet(CreateModelMixin, GenericViewSet):
  queryset = User.objects.all()
  serializer_class = UserSignUpSerializer
