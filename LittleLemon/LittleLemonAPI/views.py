from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    CategorySerializers,
    MunuItemSerializers,
    CartSerializers,
    OrderItemSerializer,
    UserSerilializer,
)
from .permissions import IsDelivery, IsCustomer, IsManager, IsDeliveryOrCustomer


class CartView(APIView):
    model = Cart
    queryset = model.objects
    serializer_class = CartSerializers
    authentication_classes = [authentication.TokenAuthentication]

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
    serializer_class = MunuItemSerializers
    authentication_classes = [authentication.TokenAuthentication]
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
