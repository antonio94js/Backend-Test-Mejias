from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from ..models import Order
from ..permissions import IsRegularUser
from .serializers import OrderSerializer


class OrderViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):

    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsRegularUser]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
