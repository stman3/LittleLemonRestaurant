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


class CartView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        cartuser = Cart.objects.filter(user=self.request.user)
        serializer_class = CartSerializers(cartuser, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id  # Set the user explicitly

        serializer_class = CartSerializers(data=data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return Response(serializer_class.data)

    def delete(self, request):
        Cart.objects.filter(user=self.request.user).delete()
        return Response("OK")
