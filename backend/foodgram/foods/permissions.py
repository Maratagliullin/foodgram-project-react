from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """Пользоватеский тип для проверка автора"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
