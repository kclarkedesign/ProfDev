from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status, viewsets, serializers
from django.contrib.auth.models import Group, User
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, GroupSerializer, MenuItemSerializer, CategorySerializer, CartSerializer
from .permissions import IsManagerGroup, IsDeliveryCrewGroup
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

# Menu-items 
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['category']
    
    

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if (self.request.method == "PUT"
            or self.request.method == "POST"
            or self.request.method == "DELETE"
        ):
            if self.request.user and self.request.user.groups.filter(name="Manager"):
                self.permission_classes = True
            else:
                self.permission_classes = False
                return Response(
                    status.HTTP_403_FORBIDDEN
                )
        return super(SingleMenuItemView, self).get_permissions()

# Create your views here.
class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class SingleGroupView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

class ManagerGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsManagerGroup]
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Manager')
    
    def post(self, request):
        # Assign user to managers group
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return Response(status=201, data={'message':'User added to Managers group'}) 


class ManagerGroupDeleteUser(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser | IsManagerGroup]

    def get_queryset(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed to the 'Manager' group"})
    
    
class DeliveryCrewGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsDeliveryCrewGroup]
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Delivery Crew')
    
    def post(self, request):
        # Assign user to managers group
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name='Delivery Crew')
            delivery_crew.user_set.add(user)
            return Response(status=201, data={'message':'User added to Delivery Crew group'})    

class DeliveryCrewGroupDeleteUser(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser | IsDeliveryCrewGroup]

    def get_queryset(self, request):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        delivery_crew = Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.remove(user)
        return Response({"message": "user removed to the 'Delivery Crew' group"})
      
@api_view()
def me(request):
    return Response(request.user.email)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = CategorySerializer
    
class SingleCategoriesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer



# example api view
# @api_view(['GET'])
# def single_group(request, id):
#     item = get_object_or_404(Group, pk=id)
#     serialized_item = GroupSerializer(item)
#     return Response(serialized_item.data)

# class CreateUserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
#     def post(self, request):
#         return Response(
#             {'message': 'user created'},
#             status=status.HTTP_201_CREATED
#         )