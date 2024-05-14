from rest_framework.permissions import BasePermission

class Authorization:

    @staticmethod
    def isManager(user):
        return user.groups.filter(name='Manager').exists()
    
    def isDeliveryCrew(user):
        return user.groups.filter(name='Delivery crew').exists()
    
    def isCustomer(user):
        return user.groups.filter(name='Customer').exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return Authorization.isManager(request.user)