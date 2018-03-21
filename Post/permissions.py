from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        """The user trying to update or delete the post must be the owner of the post"""
        return request.user and obj.user == request.user


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated
