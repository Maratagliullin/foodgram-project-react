from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddFavorites, AddShoppingCart, DownloadShoppingCart,
                    FavoritesViewSet, IngredientsViewSet, RecipeViewSet,
                    TagViewSet)

app_name = "food"

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('recipes/favorites', FavoritesViewSet, basename='favorites')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/<int:pk>/favorite/', AddFavorites.as_view()),
    path('recipes/<int:pk>/shopping_cart/', AddShoppingCart.as_view()),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls))
]
