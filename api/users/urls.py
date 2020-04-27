from rest_framework import routers
from .views import UserSignUpViewSet

app_name = 'users'

router = routers.DefaultRouter()

router.register(r'sign-up', UserSignUpViewSet)

urlpatterns = []

urlpatterns += router.urls