from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from ...orders.v1.serializers import OrderSerializer
from ..models import Menu, Option
from ..permissions import IsPublicMenuAvailable, OptionBelongsToMenu, BelongsToMe
from .serializers import MenuSerializer, OptionSerializer

class MenuViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin,  GenericViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser, BelongsToMe]

    def get_queryset(self):
        return Menu.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, url_path='orders')
    def get_orders(self, request, pk=None):
        instance = self.get_object()
        orders = Menu.objects.get_orders(pk=instance.id)
        serializer = OrderSerializer(orders, **{ 'context': self.get_serializer_context(), 'many': True})
        return Response(serializer.data)


class OptionViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser, BelongsToMe, OptionBelongsToMenu]

    def perform_create(self, serializer):
        serializer.save(menus_pk=self.kwargs.get('menus_pk'))

    def perform_update(self, serializer):
        serializer.save(menus_pk=self.kwargs.get('menus_pk'))

    def perform_destroy(self, instance):
        if Menu.objects.is_editable(pk=self.kwargs.get('menus_pk')):
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
