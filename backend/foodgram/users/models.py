from django.contrib.auth import get_user_model
from django.db import models

from foods.models import Recipe

User = get_user_model()


class ShoppingCartByUser(models.Model):
    """Список покупок пользователя"""

    current_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_to_shopping_cart',
        verbose_name='Текущий пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['current_user', 'recipe'],
                name='unique_current_user_recipe'
            )
        ]


class SubscribersByCurrentUser(models.Model):
    """Подписчики текущего пользователя"""

    current_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Текущий пользователь'
    )

    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписан'
    )

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['current_user', 'subscription'],
                name='unique_current_current_user_subscription'
            )
        ]
