from django_filters import rest_framework as filters

from foods.models import FavoritedRecipeByUser, Tag
from users.models import ShoppingCartByUser


class RecipeFilter(filters.FilterSet):
    """Фильтрация по тегу по избранному и списку покупок и автору"""
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    is_favorited = filters.BooleanFilter(method='get_is_favorited')

    def get_is_favorited(self, queryset, name, value):
        """Фильтраци по избранным, если пользователь аутентифицирован,
        то только его рецепты,если нет то все рецепты всех пользователей,
        которые находятся в избранном.
        """
        if value:
            favorited_recipes = FavoritedRecipeByUser.objects.all()
            if self.request.user.is_authenticated:
                favorite_recipe_by_users = (
                    favorited_recipes.filter(
                        current_user=self.request.user
                    ).values_list('recipe', flat=True))
                return queryset.filter(id__in=favorite_recipe_by_users)

            favorite_recipe_by_all_users = (
                favorited_recipes.values_list('recipe', flat=True))
            return queryset.filter(id__in=favorite_recipe_by_all_users)

        return queryset

    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Фильтраци по списку покупок, если пользователь аутентифицирован,
        то только его рецепты,если нет, то все рецепты всех пользователей,
        которые находятся в списке покупок.
        """
        if value:
            shopping_cart_by_user = ShoppingCartByUser.objects.all()
            if self.request.user.is_authenticated:
                favorite_recipe_by_users = shopping_cart_by_user.filter(
                    current_user=self.request.user
                ).values_list('recipe', flat=True)
                return queryset.filter(id__in=favorite_recipe_by_users)

            favorite_recipe_by_all_users = shopping_cart_by_user.values_list(
                'recipe', flat=True)
            return queryset.filter(id__in=favorite_recipe_by_all_users)

        return queryset

    author = filters.CharFilter(method='get_author')

    def get_author(self, queryset, name, value):
        if value == 'me':
            return queryset.filter(author=self.request.user)
        else:
            return queryset.filter(author=value)
