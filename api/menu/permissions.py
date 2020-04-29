from rest_framework import permissions
from django.utils.timezone import localdate


class IsPublicMenuAvailable(permissions.BasePermission):

    message = 'You cannot see a menu out of its availability date'
    """
    Object-level permission to protect the menu to be seen out of its availability day
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.available_date == localdate()
