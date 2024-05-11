from django.urls import path
from . import views

urlpatterns = [
    # User registration and token generation endpoints 
    path('users/users/me/', views.me),
    path('users/me/', views.me),
    
    # Menu-items endpoints
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    
    # User group management endpoints
    path("groups/", views.GroupView.as_view()),
    path("groups/<int:pk>/", views.SingleGroupView.as_view()),
    path("groups/manager/users/", views.ManagerGroupView.as_view(), name='manager'),
    path("groups/manager/users/<int:pk>", views.ManagerGroupView.as_view(), name='manager'),
    path("groups/delivery-crew/users/", views.DeliveryCrewGroupView.as_view(), name='delivery-crew'),
    path("groups/manager/users/<int:pk>", views.DeliveryCrewGroupView.as_view(), name='manager'),
    
    # Addition endpoint (not required)
    path('category/', views.CategoriesView.as_view()),
    path('category/<int:pk>', views.SingleMenuItemView.as_view()),
   
    # Cart management endpoints 
    path('cart/menu-items', views.CartView.as_view()),
    
    # Order management endpoints
    #path('orders', views.OrderView.as_view()),
    #path('orders<int:pk>', views.OrderView.as_view()),
]