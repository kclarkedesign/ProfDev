from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']
        
class MenuItemSerializer (serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
            model = MenuItem
            fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
    

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