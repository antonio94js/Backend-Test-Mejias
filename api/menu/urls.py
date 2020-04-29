from django.urls import include
from django.conf.urls import url
from rest_framework_nested import routers
from .views import MenuViewSet, PublicMenuViewSet, OptionViewSet

app_name = 'menu'

menu_routers = routers.SimpleRouter(trailing_slash=False)

menu_routers.register(r'menu', MenuViewSet)
menu_routers.register(r'set-menu', PublicMenuViewSet)

order_routers = routers.NestedSimpleRouter(menu_routers, r'menu', lookup='menu')
order_routers.register(r'orders', OptionViewSet)

urlpatterns = [
  url(r'^', include(menu_routers.urls)),
  url(r'^', include(order_routers.urls)),
]
  