from rest_framework import permissions

from accounts.models import NormalUser


class IsNormalUserAndOwner(permissions.BasePermission):
    """
    Custom permission for the normal user promo endpoints.
    """

    def has_object_permission(self, request, view, obj):
        """
        Only allow access to the owner of the promo in case of RETREIVE/UPDATE/DELETE
        """
        return obj.normal_user.user == request.user

    def has_permission(self, request, view):
        """
        Only allow normal users to access all the normal user endpoints.
        """
        return NormalUser.objects.filter(user=request.user).exists()
