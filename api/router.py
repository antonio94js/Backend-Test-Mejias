from django.urls import path, include

urlpatterns = [
  path('', include('api.users.urls', namespace='users')),
  path('', include('api.menu.urls', namespace='menus')),
  path('', include('api.orders.urls', namespace='orders')),
  path('', include('api.token.urls', namespace='token')),
]