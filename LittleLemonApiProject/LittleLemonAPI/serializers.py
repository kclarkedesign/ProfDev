from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Category, MenuItem, Cart, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', "name"]
        
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug', 'title']
        
class MenuItemSerializer (serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
            model = MenuItem
            fields = ['id', 'title', 'price', 'featured', 'category']
    

class CartSerializer (serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user','menu_item', 'quantity', 'unit_price', 'price']
        

class OrderSerializer (serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user','delivery_crew', 'status', 'total', 'date']
        
class OrderItemSerializer (serializers.ModelSerializer):
    #order_items = 
    
    class Meta:
        model = OrderItem
        fields = ['order','menu_item', 'quantity', 'unit_price', 'price']