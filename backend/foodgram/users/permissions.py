from rest_framework import permissions
from rest_framework.exceptions import ValidationError


class SubscribeToYourself(permissions.BasePermission):
    """Пользовательский тип для порверки подписка на самого себя"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            raise ValidationError(
                {"detail": "Подписка на самого себя запрещена"}, code=400)
        return obj != request.user
