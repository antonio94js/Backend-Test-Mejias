from rest_framework import permissions
from django.utils.timezone import localdate


class IsRegularUser(permissions.BasePermission):
    """
    Allows access only to regular users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_staff)
