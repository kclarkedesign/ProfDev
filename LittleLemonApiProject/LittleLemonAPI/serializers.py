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
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    
    class Meta:
            model = MenuItem
            fields = ['id', 'title', 'price', 'featured', 'category']
    

class CartSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    name = serializers.CharField(source='menu_item.title', read_only=True)
    
    class Meta:
        model = Cart
        fields = ['user','name', 'menu_item', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': {'read_only': True},
            'unit_price': {'read_only': True}
        }
        
class OrderItemSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields = ['order','menu_item', 'quantity', 'unit_price', 'price']

class OrderSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    order_items = OrderItemSerializer(source='orderitem_set',many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'delivery_crew', 'status', 'total', 'date']
        