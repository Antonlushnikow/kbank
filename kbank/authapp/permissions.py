from django.shortcuts import redirect
from rest_framework import permissions


class Privileged(permissions.BasePermission):
    """Привилегированные пользователи для API"""

    edit_methods = (
        "GET",
        "DELETE",
        "POST",
        "PUT",
        "PATCH",
    )

    def has_permission(self, request, view):
        if request.user.is_privileged:
            return True


class PrivilegedPermissionMixin:
    """Привилегированные пользователи"""

    def has_permissions(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_privileged
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
