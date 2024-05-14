from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    CustomerCartSerializer,
    OrderSerializer,
    UserSerializer,
    CustomerOrderItemSerializer,
    CustomerOrderSerializer,
    DeliveryCrewOrderSerializer,
)
from .models import Category, MenuItem, Cart, Order, OrderItem
from rest_framework.response import Response
from .utils.authorization import Authorization, IsManager
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User, Group
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManager]
    search_fields = ["title"]
    filterset_fields = ["title"]
    ordering_fields = ["title"]
    throttle_classes = [UserRateThrottle]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [UserRateThrottle]


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsManager]
    search_fields = ["menuitem", "quantity", "unit_price", "price"]
    filterset_fields = ["menuitem", "quantity", "unit_price", "price"]
    ordering_fields = ["menuitem", "quantity", "unit_price", "price"]
    throttle_classes = [UserRateThrottle]


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [UserRateThrottle]


class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ["title"]
    filterset_fields = ["title", "price", "featured", "category"]
    ordering_fields = ["title", "price", "featured", "category"]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def create(self, request, *args, **kwargs):

        if Authorization.isManager(request.user):
            return super().create(request, *args, **kwargs)

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )


class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):

        if Authorization.isManager(request.user):
            return super().update(request, *args, **kwargs)

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def partial_update(self, request, *args, **kwargs):
        if Authorization.isManager(request.user):
            return super().partial_update(request, *args, **kwargs)

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, *args, **kwargs):
        if Authorization.isManager(request.user):
            return super().destroy(request, *args, **kwargs)

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )


class ManagerViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def list(self, request):
        if Authorization.isManager(request.user):
            queryset = User.objects.filter(groups__name="Manager")

            username = self.request.GET.get("username")
            if username is not None:
                queryset = queryset.filter(username=username)

            search = self.request.GET.get("search")
            if search is not None:
                queryset = queryset.filter(username__icontains=search)

            ordering = self.request.GET.get("ordering")
            if ordering is not None:
                queryset = queryset.order_by(ordering)

            serialized_managers = UserSerializer(queryset, many=True)
            return Response(
                serialized_managers.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def create(self, request):
        if Authorization.isManager(request.user):
            try:
                user = User.objects.get(username=request.data["username"])
            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            groups = Group.objects.all()

            for group in groups:
                if group.name != "Manager":
                    user.groups.remove(group)
                else:
                    user.groups.add(group)

            serialized_manager = UserSerializer(user)

            return Response(
                serialized_manager.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, pk=None):
        if Authorization.isManager(request.user):
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            manager = Group.objects.get(name="Manager")
            user.groups.remove(manager)

            customer = Group.objects.get(name="Customer")
            user.groups.add(customer)

            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )


class DeliveryCrewViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    search_fields = ["username"]
    filterset_fields = ["username"]
    ordering_fields = ["username"]
    throttle_classes = [UserRateThrottle]

    def list(self, request):
        if Authorization.isManager(request.user):
            queryset = User.objects.filter(groups__name="Delivery crew")

            username = self.request.GET.get("username")
            if username is not None:
                queryset = queryset.filter(username=username)

            search = self.request.GET.get("search")
            if search is not None:
                queryset = queryset.filter(username__icontains=search)

            ordering = self.request.GET.get("ordering")
            if ordering is not None:
                queryset = queryset.order_by(ordering)

            serialized_delivery_crew = UserSerializer(queryset, many=True)
            return Response(
                serialized_delivery_crew.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def create(self, request):
        if Authorization.isManager(request.user):
            try:
                user = User.objects.get(username=request.data["username"])
            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            groups = Group.objects.all()

            for group in groups:
                if group.name != "Delivery crew":
                    user.groups.remove(group)
                else:
                    user.groups.add(group)

            serialized_delivery_crew = UserSerializer(user)

            return Response(
                serialized_delivery_crew.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def destroy(self, request, pk=None):
        if Authorization.isManager(request.user):
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            delivery_crew = Group.objects.get(name="Delivery crew")
            user.groups.remove(delivery_crew)

            customer = Group.objects.get(name="Customer")
            user.groups.add(customer)

            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )


class CustomerCartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    search_fields = ["menuitem__title", "quantity", "unit_price", "price"]
    filterset_fields = ["menuitem__title", "quantity", "unit_price", "price"]
    ordering_fields = ["menuitem__title", "quantity", "unit_price", "price"]
    throttle_classes = [UserRateThrottle]

    def list(self, request):
        queryset = Cart.objects.filter(user=request.user)

        items = request.GET.items()
        for key, value in items:
            if key in self.filterset_fields:
                queryset = queryset.filter(**{key: value})

            if key == "search":
                search_filters = Q()
                for field_name in self.search_fields:
                    search_filters |= Q(**{f"{field_name}__icontains": value})
                queryset = queryset.filter(search_filters)

            if key == "ordering" and value in self.ordering_fields:
                queryset = queryset.order_by(value)

        serialized_cart = CustomerCartSerializer(queryset, many=True)
        return Response(
            serialized_cart.data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        cart = Cart.objects.create(
            user=request.user,
            menuitem_id=request.data["menuitem"],
            quantity=request.data["quantity"],
            unit_price=request.data["unit_price"],
            price=request.data["price"],
        )

        return Response(
            CustomerCartSerializer(cart).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request):
        carts = Cart.objects.filter(user=request.user)

        for cart in carts:
            cart.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    search_fields = [
        "user__username",
        "delivery_crew__username",
        "status",
        "total",
        "date",
    ]
    filterset_fields = [
        "user__username",
        "delivery_crew__username",
        "status",
        "total",
        "date",
    ]
    ordering_fields = [
        "user__username",
        "delivery_crew__username",
        "status",
        "total",
        "date",
    ]
    throttle_classes = [UserRateThrottle]

    def list(self, request):

        if Authorization.isManager(request.user):
            queryset = Order.objects.prefetch_related("orderitem_set").all()

            items = request.GET.items()
            for key, value in items:
                if key in self.filterset_fields:
                    queryset = queryset.filter(**{key: value})

                if key == "search":
                    search_filters = Q()
                    for field_name in self.search_fields:
                        search_filters |= Q(**{f"{field_name}__icontains": value})
                    queryset = queryset.filter(search_filters)

                if key == "ordering" and value in self.ordering_fields:
                    queryset = queryset.order_by(value)

            serialized_order_items = OrderSerializer(queryset, many=True)
            return Response(serialized_order_items.data, status=status.HTTP_200_OK)

        elif Authorization.isCustomer(request.user):
            queryset = Order.objects.filter(user=request.user).prefetch_related(
                "orderitem_set"
            )

            items = request.GET.items()
            for key, value in items:
                if key in self.filterset_fields:
                    queryset = queryset.filter(**{key: value})

                if key == "search":
                    search_filters = Q()
                    for field_name in self.search_fields:
                        search_filters |= Q(**{f"{field_name}__icontains": value})
                    queryset = queryset.filter(search_filters)

                if key == "ordering" and value in self.ordering_fields:
                    queryset = queryset.order_by(value)

            serialized_order_items = CustomerOrderSerializer(queryset, many=True)

            return Response(
                serialized_order_items.data,
                status=status.HTTP_200_OK,
            )
        else:
            queryset = Order.objects.filter(
                delivery_crew=request.user
            ).prefetch_related("orderitem_set")

            items = request.GET.items()
            for key, value in items:
                if key in self.filterset_fields:
                    queryset = queryset.filter(**{key:value})

                if key == "search":
                    search_filters = Q()
                    for field_name in self.search_fields:
                        search_filters |= Q(**{f"{field_name}__icontains": value})
                    queryset = queryset.filter(search_filters)

                if key == "ordering" and value in self.ordering_fields:
                    queryset = queryset.order_by(value)

            serialized_order_items = DeliveryCrewOrderSerializer(queryset, many=True)

            return Response(
                serialized_order_items.data,
                status=status.HTTP_200_OK,
            )

    def destroy(self, request, pk=None):

        if Authorization.isManager(request.user):
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            order.delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

    def retrieve(self, request, pk=None):
        if Authorization.isCustomer(request.user):
            try:
                order = Order.objects.get(pk=pk, user=request.user)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serialized_order = CustomerOrderSerializer(order)

            return Response(
                serialized_order.data,
                status=status.HTTP_200_OK,
            )
        elif Authorization.isDeliveryCrew(request.user):
            try:
                order = Order.objects.get(pk=pk, delivery_crew=request.user)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serialized_order = DeliveryCrewOrderSerializer(order)

            return Response(
                serialized_order.data,
                status=status.HTTP_200_OK,
            )
        else:
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serialized_order = OrderSerializer(order)

            return Response(
                serialized_order.data,
                status=status.HTTP_200_OK,
            )

    def create(self, request):
        if Authorization.isCustomer(request.user):
            order = Order.objects.create(user=request.user)

            current_user_cart = Cart.objects.filter(user=request.user)

            if current_user_cart.count() == 0:
                return Response(
                    {"error": "Cart is empty"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total = 0
            for item in current_user_cart:
                OrderItem.objects.create(
                    order_id=order.id,
                    menuitem_id=item.menuitem_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price=item.price,
                )
                total += item.price
                item.delete()
            order.total = total
            order.save()

            queryset = Order.objects.prefetch_related("orderitem_set").filter(
                pk=order.id
            )
            serialized_order_items = CustomerOrderSerializer(queryset, many=True)
            return Response(
                {
                    "orders": serialized_order_items.data,
                    "message": "Order has been placed successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    def update(self, request, pk=None):
        if Authorization.isCustomer(request.user):
            try:
                order_item = OrderItem.objects.get(pk=pk)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            order_item.menuitem_id = request.data["menuitem"]
            order_item.unit_price = request.data["unit_price"]
            order_item.price = request.data["price"]
            order_item.quantity = request.data["quantity"]
            order_item.save()

            order_item_serialized = CustomerOrderItemSerializer(order_item)

            return Response(
                order_item_serialized.data,
                status=status.HTTP_201_CREATED,
            )

        elif Authorization.isManager(request.user):
            try:
                order = Order.objects.get(pk=pk)
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user = User.objects.get(pk=request.data["delivery_crew"])
            order.delivery_crew = user
            order.status = request.data["status"]
            order.save()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def partially_update(self, request, pk=None):
        if Authorization.isManager(request.user):
            try:
                order = Order.objects.get(pk=pk)

            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            order.delivery_crew = request.data["delivery_crew"]
            order.status = request.data["status"]
            order.save()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK,
            )
        elif Authorization.isDeliveryCrew(request.user):
            try:
                order = Order.objects.get(pk=pk)

            except Order.DoesNotExist:
                return Response(
                    {"error": "Order does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            order.status = request.data["status"]
            order.save()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
