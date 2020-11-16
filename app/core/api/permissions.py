from rest_framework import permissions


class AnonPermissionsOnly(permissions.BasePermission):
    """"""
    message = 'You are authenticated. Please log out and try again.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAuthenticated(permissions.BasePermission):
    """"""
    message = 'Login to continue, please'

    def has_permission(self, request, view):
        return request.user.is_authenticated