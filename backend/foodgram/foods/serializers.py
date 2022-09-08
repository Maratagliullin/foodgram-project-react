from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from foods.models import (
    FavoritedRecipeByUser, Ingredient, Recipe, RecipeIngredient, Tag
)
from users.models import ShoppingCartByUser

User = get_user_model()


class FilteredListSerializer(serializers.ListSerializer):
    """Обработка количества объектов внутри поля recipes."""

    def to_representation(self, data):
        if 'recipes_limit' in self.context['request'].query_params.keys():
            recipes_limit = (
                self.context['request'].query_params['recipes_limit'])
            if not recipes_limit.isdigit():
                raise ValidationError(
                    {'detail':
                        'recipes_limit должен содержать числовые значения'})
            data = data.all()[:int(recipes_limit)]
        data = data.all()
        return super(FilteredListSerializer, self).to_representation(data)


class AddedFavoriteSerializer(serializers.ModelSerializer):
    cooking_time = serializers.CharField(source='time', max_length=200)
    name = serializers.CharField(source='title', max_length=5000)

    class Meta:
        fields = ('cooking_time',
                  'id',
                  'name',
                  'image')
        list_serializer_class = FilteredListSerializer
        model = Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug', 'color')
        model = Tag


class RecipeIngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(
        source='recipe_ingredients.measurement_unit',)
    name = serializers.CharField(source='recipe_ingredients.title',)
    id = serializers.CharField(source='recipe_ingredients.pk',)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount',)
        model = RecipeIngredient


class RecipeIngredientCreateSerializer(serializers.Serializer):
    """Сереализатор проверки приходящих данных для ингредиентов """
    amount = serializers.CharField()
    id = serializers.IntegerField()


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов"""

    # оператор импорта перемещен на уровень класса
    # поскольку на уровне модуля сериализаторы
    # обоих приложений ссылаются друг на друга
    # соответственно получается рекурсивый импорт
    # ImportError: ...  (most likely due to a circular import)
    # для разрещения конфликта перенес на уровень класса
    from users.serializers import UserSerializer

    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)
    ingredient_title = serializers.RelatedField(
        source='ingredient.title', read_only=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(many=False)
    cooking_time = serializers.CharField(source='time', max_length=200)
    text = serializers.CharField(source='description', max_length=5000)
    name = serializers.CharField(source='title', max_length=5000)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('author', 'id', 'cooking_time',
                  'ingredients', 'tags',
                  'ingredient_title', 'name',
                  'text', 'image', 'is_favorited',
                  'is_in_shopping_cart')

        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return FavoritedRecipeByUser.objects.filter(
            recipe=obj, current_user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCartByUser.objects.filter(
            recipe=obj, current_user=user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(
        many=True,)
    cooking_time = serializers.CharField(source='time', max_length=200)
    text = serializers.CharField(source='description', max_length=5000)
    name = serializers.CharField(source='title', max_length=5000)
    image = Base64ImageField()

    class Meta:
        fields = ('cooking_time',
                  'ingredients', 'tags',
                  'name',
                  'text', 'image')
        model = Recipe


class AddedShoppingCartSerializer(serializers.ModelSerializer):
    cooking_time = serializers.CharField(source='time', max_length=200)
    name = serializers.CharField(source='title', max_length=5000)

    class Meta:
        fields = ('cooking_time',
                  'id',
                  'name',
                  'image')
        model = Recipe


class IngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, source='title')
    measurement_unit = serializers.CharField(
        source='measurement_unit.title', default='Не определено')

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )


class CreateIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title')
    measurement_unit = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = (
            'name', 'measurement_unit'
        )


class AddFavoriteSerializer(serializers.Serializer):
    """Сериализатор добавление в избранное"""

    def validate(self, attrs):
        request_user = self.context['request'].user
        recipe = self.context['recipe']

        is_favorited = (
            FavoritedRecipeByUser.objects.filter(
                current_user=request_user,
                recipe=recipe).exists())

        if is_favorited:
            raise ValidationError(
                {'detail': 'Рецепт ранее добавлен избранное'},
                code=400)

        return attrs


class DeleteFavoriteSerializer(serializers.Serializer):
    """Сериализатор удаления из избранного"""

    def validate(self, attrs):
        request_user = self.context['request'].user
        recipe = self.context['recipe']

        is_favorited = (
            FavoritedRecipeByUser.objects.filter(
                current_user=request_user,
                recipe=recipe).exists())

        if not is_favorited:
            raise ValidationError(
                {'detail': 'Рецепт отсутсвует в избранном'},
                code=400)

        return attrs


class AddShoppingCartSerializer(serializers.Serializer):
    """Сериализатор добавление в список покупок"""

    def validate(self, attrs):
        request_user = self.context['request'].user
        recipe = self.context['recipe']

        is_in_shopping_cart = (
            ShoppingCartByUser.objects.filter(
                current_user=request_user,
                recipe=recipe).exists())

        if is_in_shopping_cart:
            raise ValidationError(
                {'detail': 'Рецепт ренее добавлен в список покупок'},
                code=400)

        return attrs


class DeleteShoppingCartSerializer(serializers.Serializer):
    """Сериализатор удаления из списка покупок"""

    def validate(self, attrs):
        request_user = self.context['request'].user
        recipe = self.context['recipe']

        is_in_shopping_cart = (
            ShoppingCartByUser.objects.filter(
                current_user=request_user,
                recipe=recipe).exists())

        if not is_in_shopping_cart:
            raise ValidationError(
                {'detail': 'Рецепт отсутствует в списке покупок'},
                code=400)

        return attrs
