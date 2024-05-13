from rest_framework import permissions


class IsManagerGroup(permissions.BasePermission):
    """
    Check permission if the user is in 'Manager' group
    """

    def has_permission(self, request):
        if request.user and request.user.groups.filter(name="Manager"):
            return True
        return False


class IsDeliveryCrewGroup(permissions.BasePermission):
    """
    Check permission if the user is in 'Delivery Crew' group
    """

    def has_permission(self, request):
        if request.user and request.user.groups.filter(name="Delivery Crew"):
            return True
        return False
    

class IsAbleToModifyOrder(permissions.BasePermission):
    """
    Check permission for controlling order update
    """
    
    def has_permission(self, request):
        # Managers can modify anything, delivery crew can only update status
        if request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            return True
        if request.user.groups.filter(name='Delivery Crew').exists():
            return request.data.keys() <= {'status'}
        return False