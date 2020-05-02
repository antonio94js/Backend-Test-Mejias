from django.urls import include
from django.conf.urls import url
from rest_framework import routers
from .v1.views import OrderViewSet

app_name = 'orders'

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'orders', OrderViewSet)

urlpatterns = [
    url(r'v1/', include(router.urls)),
]
