from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]


class MunuItemSerializers(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "category", "featured"]


class CartSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, attrs):
        attrs["price"] = attrs["quantity"] * attrs["unit_price"]
        return attrs

    class Meta:
        model = Cart
        fields = ["user", "menuitem", "unit_price", "quantity", "price"]
        extra_kwargs = {"price": {"read_only": True}}


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["order", "menuitem", "quantity", "price"]


class OrderSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    OrderItem = OrderItemSerializer(many=True, read_only=True, source="order")


class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]