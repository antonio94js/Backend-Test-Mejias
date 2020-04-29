from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Menu, Option
from .serializers import MenuSerializer, OptionSerializer
from .permissions import IsPublicMenuAvailable, OrderBelongsToMenu

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

class OptionViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    permission_classes = [IsAuthenticated, OrderBelongsToMenu]

    def perform_create(self, serializer):
        serializer.save(menu_pk=self.kwargs.get('menu_pk'))

    def perform_update(self, serializer):
        serializer.save(menu_pk=self.kwargs.get('menu_pk'))

    def perform_destroy(self, instance):
        if Menu.objects.is_editable(pk=self.kwargs.get('menu_pk')):
            super().perform_destroy(instance)



class PublicMenuViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsPublicMenuAvailable]

    def permission_denied(self, request, message=None):
        """
        Override the permission_denied method to avoid raising an AuthenticationError in a public handler
        """
        raise PermissionDenied(detail=message)
