from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import (
    FavoritedRecipesByUser, Ingredient, MeasurementUnit, Recipe,
    RecipeIngredient, Tag
)
from .paginations import CustomPageNumberPagination
from .permissions import OwnerOrReadOnly
from .serializers import (
    AddedFavoriteSerializer, AddedShoppingCartSerializer,
    AddFavoriteSerializer, AddShoppingCartSerializer,
    CreateIngredientsSerializer, DeleteFavoriteSerializer,
    DeleteShoppingCartSerializer, IngredientsSerializer,
    RecipeCreateSerializer, RecipeIngredientSerializer, RecipeSerializer,
    TagSerializer
)
from .services import download_shopping_cart
from users.models import ShoppingCartByUser

User = get_user_model()


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    """Операции связананные с Ingredients"""

    lookup_field = 'id'
    serializer_class = IngredientsSerializer
    search_fields = ('=id',)
    pagination_class = None

    def get_permissions(self):
        """ Раздаем права на операции с ингредиентами"""

        if self.action in ('create'):
            return (IsAuthenticatedOrReadOnly(),)
        elif self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            return queryset.filter(title=name.lower())
        return queryset

    def create(self, request):
        serializer = CreateIngredientsSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        ingredient_list = []
        for field in serializer.validated_data:
            title = field['title']
            measurement_unit_obg, create = (
                MeasurementUnit.objects.get_or_create(
                    title=field['measurement_unit']))
            ingredient_list.append(Ingredient(
                title=title, measurement_unit=measurement_unit_obg))
        Ingredient.objects.bulk_create(ingredient_list)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoriteViewSet(viewsets.ModelViewSet):
    """Список избранного"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter


class AddFavorite(APIView):
    """Список избранного добавление/удаление"""

    def post(self, request, pk, format=None):
        recipe = get_object_or_404(
            Recipe, pk=pk)

        serializer = AddFavoriteSerializer(
            data={}, context={'request': request, 'recipe': recipe})
        serializer.is_valid(raise_exception=True)

        add_favorite = (
            FavoritedRecipesByUser(
                current_user=self.request.user, recipe=recipe))
        add_favorite.save()

        favorite_serializer = AddedFavoriteSerializer(recipe)
        return Response(favorite_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        recipe = get_object_or_404(
            Recipe, pk=pk)

        serializer = DeleteFavoriteSerializer(
            data={}, context={'request': request, 'recipe': recipe})
        serializer.is_valid(raise_exception=True)

        del_to_favorite = FavoritedRecipesByUser.objects.filter(
            current_user=self.request.user, recipe=recipe)
        del_to_favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AddShoppingCart(APIView):
    """Корзина покупок добвление/удаление"""

    def post(self, request, pk, format=None):
        recipe = get_object_or_404(
            Recipe, pk=pk)

        serializer = AddShoppingCartSerializer(
            data={}, context={'request': request, 'recipe': recipe})
        serializer.is_valid(raise_exception=True)

        add_to_shopping_cart = (
            ShoppingCartByUser(
                current_user=self.request.user, recipe=recipe))
        add_to_shopping_cart.save()

        recipe_serializer = AddedShoppingCartSerializer(recipe)
        return Response(recipe_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        recipe = get_object_or_404(
            Recipe, pk=pk)

        serializer = DeleteShoppingCartSerializer(
            data={}, context={'request': request, 'recipe': recipe})
        serializer.is_valid(raise_exception=True)

        add_to_shopping_cart = ShoppingCartByUser.objects.filter(
            current_user=self.request.user, recipe=recipe)

        add_to_shopping_cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        """ Раздаем права на просмотр пользователей
        и регистрацию пользователей"""

        if self.action in ('partial_update', 'destroy'):
            return (OwnerOrReadOnly(),)
        elif self.action in ('list', 'retrieve'):
            return (AllowAny(),)
        return super().get_permissions()

    def create(self, request):
        """Создание рецепта"""

        serializer = RecipeCreateSerializer(data=request.data)
        if serializer.is_valid():
            ingredients = serializer.validated_data['ingredients']
            tags = serializer.validated_data['tags']
            image = serializer.validated_data['image']
            title = serializer.validated_data['title']
            description = serializer.validated_data['description']
            time = serializer.validated_data['time']
            recipe = Recipe(author=self.request.user,
                            title=title,
                            image=image,
                            description=description,
                            time=time,)
            recipe.save()

            for tag in tags:
                recipe.tags.add(tag)

            # Разбор инредиентов из данных post запроса
            for ingredient in ingredients:
                object_ingredient = get_object_or_404(
                    Ingredient, id=ingredient['id'])
                recipe_ingredient = RecipeIngredient(
                    amount=ingredient['amount'],
                    recipe=recipe,
                    recipe_ingredients=object_ingredient)
                recipe_ingredient.save()

                recipe_serializer = RecipeSerializer(
                    recipe, context={'request': request})

            return Response(recipe_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        """Обновление рецепта"""
        recipe = get_object_or_404(Recipe, id=pk)

        # For has_object_permission on partial_update
        # https://www.django-rest-framework.org/api-guide/generic-views/#get_objectself
        self.get_object()

        serializer = RecipeCreateSerializer(
            recipe, data=request.data,
            context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        RecipeIngredient.objects.filter(recipe=recipe).delete()
        ingredients = serializer.data['ingredients']
        for ingredient in ingredients:
            object_ingredient = get_object_or_404(
                Ingredient, id=ingredient['id'])
            recipe_ingredient = RecipeIngredient(
                amount=ingredient['amount'],
                recipe=recipe,
                recipe_ingredients=object_ingredient)
            recipe_ingredient.save()

            recipe_serializer = RecipeSerializer(
                recipe, context={'request': request})

        recipe_serializer = RecipeSerializer(
            recipe, context={'request': request})
        return Response(recipe_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """Удаление рецепта"""

        recipe = get_object_or_404(Recipe, id=pk)

        # For has_object_permission on partial_update
        # https://www.django-rest-framework.org/api-guide/generic-views/#get_objectself
        self.get_object()
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги"""

    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class DownloadShoppingCart(APIView):
    """Выгрузка списка покупок"""

    def get(self, request, format=None):
        result_string = download_shopping_cart(request)
        return HttpResponse(result_string,
                            content_type='text/plain',
                            status=status.HTTP_200_OK)
