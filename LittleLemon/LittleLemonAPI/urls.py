from django.urls import path
from .views import CartView, MenuItemsView

urlpatterns = [
    path("menu-items/", MenuItemsView.as_view(), name="menu items view"),
    path("cart/menu-items/", CartView.as_view(), name="CartView"),
]
