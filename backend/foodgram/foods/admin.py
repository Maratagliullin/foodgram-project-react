from django.contrib import admin

from .models import (
    FavoritedRecipeByUser, Ingredient, MeasurementUnit, Recipe,
    RecipeIngredient, Tag
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)

    list_display = ('title', 'in_favorites', 'author', 'pub_date')
    readonly_fields = ('in_favorites',)
    list_filter = ('author', 'title', 'tags')

    def in_favorites(self, obj):
        return FavoritedRecipeByUser.objects.filter(recipe=obj).count()

    in_favorites.short_description = 'Находится списке избранного (количество)'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'recipe_ingredients', 'recipe_id',)

    @admin.display(
        description='Рецепт',
    )
    def recipe_id(self, obj):
        return obj.recipe.id


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'measurement_unit')
    list_filter = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(FavoritedRecipeByUser)
class FavoritedRecipeByUsersAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'recipe')
