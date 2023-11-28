from django.urls import path
from .views import ListUsers, CartView

urlpatterns = [
    path("list-users/", ListUsers.as_view(), name="list-users"),
    path("cart/menu-items/", CartView.as_view(), name="CartView"),
]
