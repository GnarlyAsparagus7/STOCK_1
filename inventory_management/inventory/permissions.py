# inventory/permissions.py

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    Assumes that `Profile` has an `is_admin` field.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsStaff(permissions.BasePermission):
    """
    Allows access only to staff users.
    Assumes that `Profile` has an `is_staff` field.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.profile.is_staff)


class IsRegularUser(permissions.BasePermission):
    """
    Allows access only to regular users.
    Assumes that `Profile` has an `is_regular_user` field.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.profile.is_regular_user)
