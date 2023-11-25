from django.urls import path
from .views import ListUsers

urlpatterns = [
    path("list-users/", ListUsers.as_view(), name="list-users"),
]
