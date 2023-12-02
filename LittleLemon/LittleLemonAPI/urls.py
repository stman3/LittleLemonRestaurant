from django.urls import path
from .views import CartView, MenuItemsView, MenuItemSingalView, GroupView

urlpatterns = [
    path("menu-items/", MenuItemsView.as_view(), name="menu items view"),
    path("cart/menu-items/", CartView.as_view(), name="CartView"),
    path(
        "menu-items/<int:pk>",
        MenuItemSingalView.as_view(),
        name="Menu item singal",
    ),
    path("groups/manager/users", GroupView.as_view(), name="Group view"),
]
