from django.urls import path
from .views import (
    CartView,
    MenuItemsView,
    MenuItemSingalView,
    GroupView,
    GroupDetailView,
    DeliveryView,
    DeliveryDetailView,
)

urlpatterns = [
    path("menu-items/", MenuItemsView.as_view(), name="menu items view"),
    path("cart/menu-items/", CartView.as_view(), name="CartView"),
    path(
        "menu-items/<int:pk>",
        MenuItemSingalView.as_view(),
        name="Menu item singal",
    ),
    path("groups/manager/users", GroupView.as_view(), name="Group view"),
    path(
        "groups/manager/users/<int:pk>",
        GroupDetailView.as_view(),
        name="Group Detail View",
    ),
    path("groups/delivery-crew/users", DeliveryView.as_view(), name="Group view"),
    path(
        "groups/delivery-crew/users/<int:pk>",
        DeliveryDetailView.as_view(),
        name="Group Detail View",
    ),
]
