from rest_framework.permissions import BasePermission, SAFE_METHODS


class QuestionPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        """The user trying to update or delete the post must be the owner of the question"""
        return request.user and obj.author == request.user
