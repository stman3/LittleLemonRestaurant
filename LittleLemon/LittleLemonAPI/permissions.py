from rest_framework.permissions import BasePermission


class IsDelivery(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="delivery crew").exists()


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Customer").exists()


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()


class IsDeliveryOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(
            name__in=["delivery crew", "Customer"]
        ).exists()
