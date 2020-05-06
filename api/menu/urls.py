from django.urls import include
from django.conf.urls import url
from rest_framework_nested import routers
from .v1.views import MenuViewSet, PublicMenuViewSet, OptionViewSet

app_name = 'menu'

menu_routers = routers.SimpleRouter(trailing_slash=False)

menu_routers.register(r'menus', MenuViewSet)
menu_routers.register(r'daily-menu', PublicMenuViewSet, basename='daily-menu')


option_routers = routers.NestedSimpleRouter(menu_routers, r'menus', lookup='menus')
option_routers.register(r'options', OptionViewSet)

urlpatterns = [
    url(r'v1/', include(menu_routers.urls)),
    url(r'v1/', include(option_routers.urls)),
]
