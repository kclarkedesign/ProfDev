from django.urls import path
from . import views


urlpatterns = [
    path("menu-items", views.MenuItemList.as_view(), name="menu-items"),
    path(
        "menu-items/<int:pk>", views.MenuItemDetail.as_view(), name="menu-items-detail"
    ),
    path("categories", views.CategoryList.as_view(), name="categories"),
    path(
        "categories/<int:pk>", views.CategoryDetail.as_view(), name="categories-detail"
    ),
    path("carts", views.CartList.as_view(), name="carts"),
    path("carts/<int:pk>", views.CartDetail.as_view(), name="carts-detail"),
    path(
        "cart/menu-items",
        views.CustomerCartViewSet.as_view(
            {
                "get": "list",
                "post": "create",
                "delete": "destroy",
            }
        ),
        name="cart-menu-items",
    ),
    path(
        "orders",
        views.OrderViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="order-items",
    ),
    path(
        "orders/<int:pk>",
        views.OrderViewSet.as_view(
            {
                "delete": "destroy",
                "get": "retrieve",
                "put": "update",
                "patch": "partially_update"
            }
        ),
        name="order-items-detail",
    ),
    path(
        "groups/manager/users",
        views.ManagerViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="managers",
    ),
    path(
        "groups/manager/users/<int:pk>",
        views.ManagerViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
        name="managers-detail",
    ),
    path(
        "groups/delivery-crew/users",
        views.DeliveryCrewViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="delivery-crew",
    ),
    path(
        "groups/delivery-crew/users/<int:pk>",
        views.DeliveryCrewViewSet.as_view(
            {
                "delete": "destroy",
            }
        ),
        name="delivery-crew-detail",
    ),
]
