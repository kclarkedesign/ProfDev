from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer as DjoserUserSerializer,
)
from django.contrib.auth.models import Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class CustomerCartSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.StringRelatedField(source="menuitem", read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source="menuitem", write_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "menu_item_name",
            "menu_item_id",
            "quantity",
            "unit_price",
            "price",
        ]


class CartSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.StringRelatedField(source="menuitem", read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source="menuitem", write_only=True
    )

    class Meta:
        model = Cart
        exclude = ["menuitem"]


class UserSerializer(DjoserUserSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["groups"] = instance.groups.values_list("name", flat=True)
        return representation


class UserRegistrationSerializer(UserCreateSerializer):
    def save(self, **kwargs):
        user = super().save(**kwargs)
        customer_group = Group.objects.get(name="Customer")
        customer_group.user_set.add(user)
        return user


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "unit_price", "price"]
        validators = [
            UniqueTogetherValidator(
                queryset=OrderItem.objects.all(),
                fields=["order", "menuitem"],
                message="This item is already in the order",
            )
        ]

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    orderitem = OrderItemSerializer(many=True, read_only=True, source="orderitem_set")

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'date', 'orderitem', 'user', 'delivery_crew']

class CustomerOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "unit_price", "price"]
        validators = [
            UniqueTogetherValidator(
                queryset=OrderItem.objects.all(),
                fields=["order", "menuitem"],
                message="This item is already in the order",
            )
        ]

class CustomerOrderSerializer(serializers.ModelSerializer):
    orderitem = CustomerOrderItemSerializer(many=True, read_only=True, source="orderitem_set")
    status = serializers.BooleanField(read_only=True)
    date = serializers.DateField(read_only=True)
    delivery_crew = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'date', 'orderitem', 'delivery_crew']



class DeliveryCrewOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "unit_price", "price"]
        validators = [
            UniqueTogetherValidator(
                queryset=OrderItem.objects.all(),
                fields=["order", "menuitem"],
                message="This item is already in the order",
            )
        ]


class DeliveryCrewOrderSerializer(serializers.ModelSerializer):
    orderitem = DeliveryCrewOrderItemSerializer(many=True, read_only=True, source="orderitem_set")

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'date', 'orderitem', 'user']
