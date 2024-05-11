from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, serializers
from django.contrib.auth.models import Group, User
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, GroupSerializer, MenuItemSerializer, CategorySerializer, CartSerializer

# Create your views here.
class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class SingleGroupView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    
class ManagerGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Manager')
    
class DeliveryCrewGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Delivery Crew')

# example api view
# @api_view(['GET'])
# def single_group(request, id):
#     item = get_object_or_404(Group, pk=id)
#     serialized_item = GroupSerializer(item)
#     return Response(serialized_item.data)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoriesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['category']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

@api_view()
def me(request):
    return Response(request.user.email)

