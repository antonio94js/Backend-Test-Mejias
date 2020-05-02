from rest_framework import permissions
from django.utils.timezone import localdate


class IsPublicMenuAvailable(permissions.BasePermission):

    message = 'You cannot see a menu out of its availability date'

    """
    Object-level permission to protect any menu to be seen out of its availability day
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.available_date == localdate()


class OrderBelongsToMenu(permissions.BasePermission):

    EDIT_METHODS = ['PUT', 'DELETE']
    
    message = 'This order doesn\'t belong to this menu'

    """
    Object-level permission to check that any action performed over any menus option belongs to the proper menu 
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in self.EDIT_METHODS:
            return str(obj.menu.id) == view.kwargs.get('menu_pk')
        return True

class BelongsToMe(permissions.BasePermission):

    EDIT_METHODS = ['PUT', 'DELETE', 'POST']
    
    message = 'This menu doesn\'t belong to you'

    # This Permission class assumes that there could be more 'super users' creating menus going forward

    """
    Object-level permission to protect that nobody may be able to edit other's menu
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in self.EDIT_METHODS:
            return obj.get_user() == request.user
        return True
