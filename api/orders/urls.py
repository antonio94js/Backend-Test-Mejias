from rest_framework import routers
from django.urls import include
from django.conf.urls import url
from .views import OrderViewSet

app_name = 'orders'

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'orders', OrderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
