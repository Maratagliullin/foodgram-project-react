from django.contrib.auth import get_user_model
from django.db import models

from food.models import Recipe

User = get_user_model()


class FavoritedRecipesByUser(models.Model):
    """Избранные рецепты пользователя"""

    current_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_to_favorited',
        verbose_name='Текущий пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Список избранного'
        unique_together = ['current_user', 'recipe']


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
        unique_together = ['current_user', 'recipe']


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
        unique_together = ['current_user', 'subscription']
