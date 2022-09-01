from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from food.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import (FavoritedRecipesByUser, ShoppingCartByUser,
                          SubscribersByCurrentUser)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор вывода данных пользователя"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if SubscribersByCurrentUser.objects.filter(
                current_user=user, subscription=obj).exists():
            return True
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
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
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True)
    ingredient_title = serializers.RelatedField(
        source='ingredient.title', read_only=True)
    tags = TagSerializer(many=True)
    author = UserSerializer()
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
        is_favorited = FavoritedRecipesByUser.objects.filter(
            recipe=obj, current_user=user).exists()

        if is_favorited:
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        in_shopping_cart = ShoppingCartByUser.objects.filter(
            recipe=obj, current_user=user).exists()

        if in_shopping_cart:
            return True
        return False


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
        fields = [
            'id', 'name', 'measurement_unit'
        ]


class CreateIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title')
    measurement_unit = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = [
            'name', 'measurement_unit'
        ]
