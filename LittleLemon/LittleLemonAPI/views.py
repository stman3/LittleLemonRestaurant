from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User, Group
from datetime import date
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    CategorySerializers,
    MenuItemSerializers,
    CartSerializers,
    OrderItemSerializer,
    UserSerilializer,
    OrderSerializers,
)
from .permissions import IsDelivery, IsCustomer, IsManager, IsDeliveryOrCustomer

from django.views.decorators.csrf import csrf_exempt


class CartView(APIView):
    model = Cart
    queryset = model.objects
    serializer_class = CartSerializers
    permission_classes = [IsCustomer]

    def get(self, request):
        cartuser = self.queryset.filter(user=request.user)
        cart_object = self.serializer_class(cartuser, many=True)
        return Response(cart_object.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        cart_object = self.serializer_class(data=data)
        cart_object.is_valid(raise_exception=True)
        cart_object.save()
        return Response(cart_object.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        self.queryset.filter(user=self.request.user).delete()
        return Response("Cart have been delete it ", status=status.HTTP_200_OK)


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
    queryset = model.objects
    serializer_class = MenuItemSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsManager()]

        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        pk_value = kwargs.get("pk")
        try:
            menu_item = self.queryset.get(id=pk_value)
            MenuItem_object = self.serializer_class(menu_item)
            return Response(MenuItem_object.data)
        except self.model.DoesNotExist:
            return Response(
                {"error": "Menu item is not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, reqeust, *args, **kwargs):
        try:
            menu_item = self.queryset.get(id=kwargs.get("pk"))
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
            menu_item = self.queryset.get(id=kwargs.get("pk"))
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
            menu_item = self.queryset.get(id=kwargs.get("pk"))
        except self.model.DoesNotExist:
            return Response(
                {"error": "Menu item is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        MenuItem_oject = self.serializer_class(menu_item)
        menu_item.delete()
        return Response(MenuItem_oject.data, status=status.HTTP_200_OK)


class GroupView(APIView):
    model = User
    queryset = model.objects
    permission_classes = [IsManager]
    serializer_class = UserSerilializer
    group = Group.objects.get(name="Manager")

    def get(self, request):
        user = self.queryset.filter(groups__name="Manager")
        user_object = self.serializer_class(user, many=True)

        return Response(user_object.data)

    def post(self, request):
        usernameValue = request.data["username"]
        try:
            user = self.queryset.get(username=usernameValue)
        except self.model.DoesNotExist:
            return Response(
                {"error": "User name  is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.groups.add(self.group)
        return Response("done", status=status.HTTP_200_OK)


class GroupDetailView(APIView):
    model = User
    queryset = model.objects
    permission_classes = [IsManager]
    serializer_class = UserSerilializer
    group = Group.objects.get(name="Manager")

    def delete(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(id=kwargs.get("pk"))
        except self.model.DoesNotExist:
            return Response(
                {"error": "User name  is not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.groups.filter(name="Manager").exists():
            user.groups.remove(self.group)

            return Response("ok")

        return Response(
            {"error": "User is not Manger"}, status=status.HTTP_404_NOT_FOUND
        )


class DeliveryView(APIView):
    model = User
    queryset = model.objects
    permission_classes = [IsManager]
    serializer_class = UserSerilializer
    group = Group.objects.get(name="delivery crew")

    def get(self, request):
        user = self.queryset.filter(groups__name="delivery crew")
        user_object = self.serializer_class(user, many=True)

        return Response(user_object.data)

    def post(self, request):
        usernameValue = request.data["username"]
        try:
            user = self.queryset.get(username=usernameValue)
        except self.model.DoesNotExist:
            return Response(
                {"error": "User name  is not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.groups.add(self.group)
        return Response("done", status=status.HTTP_200_OK)


class DeliveryDetailView(APIView):
    model = User
    queryset = model.objects
    permission_classes = [IsManager]
    serializer_class = UserSerilializer
    group = Group.objects.get(name="delivery crew")

    def delete(self, request, *args, **kwargs):
        try:
            user = self.queryset.get(id=kwargs.get("pk"))
        except self.model.DoesNotExist:
            return Response(
                {"error": "User name  is not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.groups.filter(name="delivery crew").exists():
            user.groups.remove(self.group)

            return Response("ok")

        return Response(
            {"error": "User is not Manger"}, status=status.HTTP_404_NOT_FOUND
        )


class OrderView(APIView):
    model = OrderItem
    queryser = model.objects
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post_permissions(self):
        if self.request.method == "POST":
            return [IsCustomer()]
        return super().get_permissions()

    def post(self, request):
        try:
            Cartitem = Cart.objects.filter(user=request.user)
            total = 0
            if not Cartitem.exists:
                return Response("no item in the Cart", status=status.HTTP_404_NOT_FOUND)
            for cart in Cartitem:
                total += cart.price
            data = {
                "user": request.user.id,
                "total": total,
                "status": False,
                "date": date.today(),
            }

            order_serializer = OrderSerializers(data=data)
            if order_serializer.is_valid(raise_exception=True):
                order = order_serializer.save()
                for item in Cartitem:
                    menuitem = MenuItem.objects.get(id=item.menuitem_id)

                    dataI = {
                        "order": order.id,
                        "menuitem": menuitem.pk,
                        "quantity": item.quantity,
                        "price": item.price,
                    }
                    orderitem_object = OrderItemSerializer(data=dataI)
                    orderitem_object.is_valid(raise_exception=True)
                    orderitem_object.save()

                Cartitem.delete()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except self.model.DoesNotExist:
            return Response(
                {"error": "User name  is not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request):
        try:
            user = request.user

            if IsManager().has_permission(request, self):
                orders = Order.objects.all()
            elif IsCustomer().has_permission(request, self):
                orders = Order.objects.filter(user=user)
            elif IsDelivery().has_permission(request, self):
                orders = Order.objects.filter(delivery_crew=user)
            else:
                return Response(
                    {"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN
                )

            serializer = OrderSerializers(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response(
                {"error": "User has no orders"}, status=status.HTTP_404_NOT_FOUND
            )


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_order(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
            return order
        except Order.DoesNotExist:
            return None

    def get(self, request, orderId):
        try:
            order = self.get_order(orderId)
            if order and (
                IsCustomer().has_object_permission(request, self, order)
                or IsManager().has_permission(request, self)
            ):
                serializer = OrderSerializers(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "Order not found or permission denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, orderId):
        try:
            order = self.get_order(orderId)
            if order and IsDelivery().has_permission(request, self):
                data = request.data
                order.status = data.get("status", order.status)
                order.save()
                serializer = OrderSerializers(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "Order not found or permission denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, orderId):
        try:
            order = self.get_order(orderId)
            if order and IsManager().has_permission(request, self):
                order.delete()
                return Response(
                    {"message": "Order deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            return Response(
                {"error": "Order not found or permission denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, orderId):
        try:
            order = self.get_order(orderId)
            if order and IsCustomer().has_object_permission(request, self, order):
                data = request.data
                order.delivery_crew = data.get("delivery_crew", order.delivery_crew)
                order.status = data.get("status", order.status)
                order.save()
                serializer = OrderSerializers(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "Order not found or permission denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
