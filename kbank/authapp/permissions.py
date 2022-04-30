from rest_framework import permissions


class Privileged(permissions.BasePermission):
    """ Привилегированные пользователи"""

    edit_methods = ("GET", "DELETE", "POST", "PUT", "PATCH", )

    def has_permission(self, request, view):
        if request.user.is_privileged:
            return True
