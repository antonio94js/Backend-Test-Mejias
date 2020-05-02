from django.urls import include
from django.conf.urls import url
from rest_framework import routers
from .v1.views import UserSignUpViewSet

app_name = 'users'

router = routers.DefaultRouter()

router.register(r'sign-up', UserSignUpViewSet)

urlpatterns = [
  url(r'v1/', include(router.urls)),
]