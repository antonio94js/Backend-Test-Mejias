from rest_framework import permissions
from django.utils.timezone import localdate


class IsPublicMenuAvailable(permissions.BasePermission):

    message = 'You cannot see a menu out of its availability date'
    """
    Object-level permission to protect the menu to be seen out of its availability day
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.available_date == localdate()


class OrderBelongsToMenu(permissions.BasePermission):

    EDIT_METHODS = ['PUT', 'DELETE']
    
    message = 'This order doesn\'t belong to this menu'

    """
    Object-level permission to protect the menu 
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in self.EDIT_METHODS:
            return str(obj.menu.id) == view.kwargs.get('menu_pk')
        return True
