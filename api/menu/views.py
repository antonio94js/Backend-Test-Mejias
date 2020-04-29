from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Menu, Option
from .serializers import MenuSerializer, OptionSerializer
from .permissions import IsPublicMenuAvailable

class MenuViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin,  GenericViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class OptionViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.kwargs)
        serializer.save(menu_pk=self.kwargs.get('menu_pk'))
    def perform_update(self, serializer):
        print(self.kwargs)
        serializer.save(menu_pk=self.kwargs.get('menu_pk'))



class PublicMenuViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsPublicMenuAvailable]

    def permission_denied(self, request, message=None):
        """
        Override the permission_denied method to avoid raising an AuthenticationError in a public handler
        """
        raise PermissionDenied(detail=message)
