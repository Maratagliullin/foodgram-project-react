from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .services import DownloadShoppingCart
from .views import (
    AddFavorite, AddShoppingCart, FavoriteViewSet, IngredientViewSet,
    RecipeViewSet, TagViewSet
)

app_name = 'foods'

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('recipes/favorites', FavoriteViewSet, basename='favorites')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/<int:pk>/favorite/', AddFavorite.as_view()),
    path('recipes/<int:pk>/shopping_cart/', AddShoppingCart.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls))
]
