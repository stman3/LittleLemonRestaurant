from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    CategorySerializers,
    MenuItemSerializers,
    CartSerializers,
    OrderItemSerializer,
    UserSerilializer,
)
from .permissions import IsDelivery, IsCustomer, IsManager, IsDeliveryOrCustomer


class CartView(APIView):
    model = Cart
    queryset = model.objects
    serializer_class = CartSerializers
    permission_classes = [IsCustomer]

    def get(self, request):
        cartuser = self.queryset.filter(user=request.user)
        cart_object = self.serializer_class(cartuser, many=True)
        return Response(cart_object.data)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        cart_object = self.serializer_class(data=data)
        cart_object.is_valid(raise_exception=True)
        cart_object.save()
        return Response(cart_object.data)

    def delete(self, request):
        self.queryset.filter(user=self.request.user).delete()
        return Response("OK")


class MenuItemsView(APIView):
    model = MenuItem
    queryset = model.objects
    serializer_class = MenuItemSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return super().get_permissions()

    def get(self, request):
        return Response(
            self.serializer_class(self.queryset.all(), many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        MenuItem_object = self.serializer_class(data=request.data)
        MenuItem_object.is_valid(raise_exception=True)
        MenuItem_object.save()
        return Response(MenuItem_object.data, status=status.HTTP_201_CREATED)


class MenuItemSingalView(APIView):
    model = MenuItem
    qureyset = model.objects
    serializer_class = MenuItemSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsManager()]

        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        pk_value = kwargs.get("pk")
        try:
            menu_item = self.qureyset.get(id=pk_value)
            MenuItem_object = self.serializer_class(menu_item)
            return Response(MenuItem_object.data)
        except self.model.DoesNotExist:
            return Response(
                {"error": "Menu item is not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, reqeust, *args, **kwargs):
        try:
            menu_item = self.qureyset.get(id=kwargs.get("pk"))
        except self.model.DoesNotExist:
            return Response(
                {"error": "Menu item is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        MenuItem_object = self.serializer_class(menu_item, data=reqeust.data)
        if MenuItem_object.is_valid():
            MenuItem_object.save()
            return Response(MenuItem_object.data, status=status.HTTP_200_OK)
        return Response(MenuItem_object.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, reqeust, *args, **kwargs):
        try:
            menu_item = self.qureyset.get(id=kwargs.get("pk"))
        except self.model.DoesNotExist:
            return Response(
                {"error": "Menu item is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        MenuItem_object = self.serializer_class(
            menu_item, data=reqeust.data, partial=True
        )
        if MenuItem_object.is_valid():
            MenuItem_object.save()
            return Response(MenuItem_object.data, status=status.HTTP_200_OK)
        return Response(MenuItem_object.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, reqeust, *args, **kwargs):
        try:
            menu_item = self.qureyset.get(id=kwargs.get("pk"))
        except self.model.DoesNotExist:
            return Response(
                {"error": "Menu item is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        MenuItem_oject = self.serializer_class(menu_item)
        menu_item.delete()
        return Response(MenuItem_oject.data, status=status.HTTP_200_OK)
