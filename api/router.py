from django.urls import path, include

urlpatterns = [
  path('', include('api.users.urls', namespace='users'))
]