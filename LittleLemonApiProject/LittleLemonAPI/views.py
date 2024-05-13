from django.shortcuts import get_object_or_404
from datetime import date
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status, viewsets, serializers
from django.contrib.auth.models import Group, User
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, GroupSerializer, MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer
from .permissions import IsManagerGroup, IsDeliveryCrewGroup
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Menu-items 
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'category']
    filterset_fields = ['price', 'inventory']
    search_fields = ['category']
    
    def get_permissions(self):        
        if self.request.method != 'GET':
            permission_classes = [IsManagerGroup | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
            
        return[permission() for permission in permission_classes]
     

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsManagerGroup | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
        

# User group management endpoints
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
            return Response({'message':'User added to Managers group'}, status=status.HTTP_201_CREATED) 


class ManagerGroupDeleteUser(generics.DestroyAPIView):
    permission_classes = [IsAdminUser | IsManagerGroup]

    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if user in managers.user_set.all():
            managers.user_set.remove(user)
            return Response({"message": "User removed from the 'Manager' group"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not in 'Manager' group"}, status=status.HTTP_404_NOT_FOUND)
    
    
class DeliveryCrewGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser | IsManagerGroup]
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Delivery Crew')
    
    def post(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name='Delivery Crew')
            delivery_crew.user_set.add(user)
            return Response({'message':'User added to Delivery Crew group'}, status=status.HTTP_201_CREATED) 
            

class DeliveryCrewGroupDeleteUser(generics.DestroyAPIView):
    permission_classes = [IsAdminUser | IsManagerGroup]

    def delete(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)
        delivery_crew = Group.objects.get(name="Delivery Crew")
        if user in delivery_crew.user_set.all():
            delivery_crew.user_set.remove(user)
            return Response({"message": "User removed from the 'Delivery Crew' group"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not in 'Delivery Crew' group"}, status=status.HTTP_404_NOT_FOUND)

# for Addition endpoint (not required)
class CategoriesView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = CategorySerializer
    
class SingleCategoriesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# for Cart management endpoints
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        menu_item = self.request.data.get('menu_item')
        quantity = self.request.data.get('quantity')
        unit_price = MenuItem.objects.get(pk=menu_item).price
        quantity = int(quantity)
        price = quantity * unit_price
        serializer.save(user=self.request.user, unit_price=unit_price, price=price)
        
    def delete(self, request, *args, **kwargs):
        cart = self.get_queryset()
        
        if cart.exists():
            cart.delete()
            return Response({"message": "Items removed from cart"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Items not found"}, status=status.HTTP_404_NOT_FOUND)
     

# for Order management endpoints
class OrderView(generics.ListCreateAPIView):
    
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser == True :
            return Order.objects.all().prefetch_related('orderitem_set')
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user).prefetch_related('orderitem_set')
        else:
            return Order.objects.filter(user=self.request.user).prefetch_related('orderitem_set')
    
    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        total = Decimal(0)
        
        for item in cart_items:
            total += item.price
        
        order = Order.objects.create(user=request.user, status=0, total=total, date=date.today())
        for item in cart_items.values():
            menu_item = get_object_or_404(MenuItem, id=item['id'])
            orderitem = OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item['quantity'], unit_price=item['unit_price'], price=item['price'])
            orderitem.save()
            
        cart_items.delete()
        return Response({"message": "Your order has been placed and on the way"}, status=status.HTTP_201_CREATED)
        
        
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, order) 
        return order          
    
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.groups.filter(name='Delivery Crew').exists():
            # Allow only status updates by Delivery Crew
            if set(request.data.keys()) > {'status'}:
                return Response({'detail': 'You are only allowed to update the status.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return self.partial_update(request, *args, **kwargs)
        
        elif request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            # Managers can update delivery crew and status
            return self.partial_update(request, *args, **kwargs)
        
        return Response({'detail': 'Not authorized to update this order.'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            self.update(request, *args, **kwargs)
            return Response({'message': 'Order updated'}, status=status.HTTP_200_OK) 
        return Response({'message': 'Not authorized to fully update this order.'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            self.destroy(request, *args, **kwargs)
            return Response({'message': 'Order deleted'}, status=status.HTTP_204_OK) 
        
        return Response({'message': 'Not authorized to delete this order.'}, status=status.HTTP_403_FORBIDDEN)
        

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

# @api_view()
# def me(request):
#     return Response(request.user.email)