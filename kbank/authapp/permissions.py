from rest_framework import permissions


class Privileged(permissions.BasePermission):
    """ Привилегированные пользователи"""

    edit_methods = ("GET", "DELETE", "POST", "PUT", "PATCH", )

    def has_permission(self, request, view):
        if request.user.is_privileged:
            return True


class PrivilegedPermissionMixin:
    def has_permissions(self):
        return self.request.user.is_privileged

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
