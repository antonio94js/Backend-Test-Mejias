from django.urls import include
from django.conf.urls import url
from rest_framework_nested import routers
from .v1.views import MenuViewSet, PublicMenuViewSet, OptionViewSet

app_name = 'menu'

menu_routers = routers.SimpleRouter(trailing_slash=False)

menu_routers.register(r'menu', MenuViewSet)
menu_routers.register(r'set-menu', PublicMenuViewSet)

option_routers = routers.NestedSimpleRouter(menu_routers, r'menu', lookup='menu')
option_routers.register(r'options', OptionViewSet)

urlpatterns = [
    url(r'v1/', include(menu_routers.urls)),
    url(r'v1/', include(option_routers.urls)),
]
