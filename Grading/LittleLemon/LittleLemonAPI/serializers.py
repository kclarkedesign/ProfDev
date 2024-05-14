from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = [
            'id', 
            'quantity', 
            'unit_price', 
            'price', 
            'user_id', 
            'user', 
            'menuitem_id', 
            'menuitem',
        ]
        extra_kwargs = {
            'quantity': { 'min_value': 1 },
        }

class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total',
            'date',
            'user_id',
            'user',
            'delivery_crew_id',
            'delivery_crew',
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    order = OrderSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'quantity',
            'unit_price',
            'price',
            'order_id',
            'order',
            'menuitem_id', 
            'menuitem',
        ]
        extra_kwargs = {
            'quantity': { 'min_value': 1 }
        }