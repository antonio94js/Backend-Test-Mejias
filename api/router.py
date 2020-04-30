from django.urls import path, include

urlpatterns = [
  path('', include('api.users.urls', namespace='users')),
  path('', include('api.menu.urls', namespace='menu')),
  path('', include('api.orders.urls', namespace='orders')),
]