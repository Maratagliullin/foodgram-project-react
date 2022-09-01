from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag, Units
from users.models import FavoritedRecipesByUser


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)

    list_display = (
        'title', 'in_favorites', 'author', 'pub_date')
    readonly_fields = ('in_favorites',)
    list_filter = ('author', 'title', 'tags')

    def in_favorites(self, obj):
        return FavoritedRecipesByUser.objects.filter(recipe=obj).count()

    in_favorites.short_description = 'Находится списке избранного (количество)'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe', 'recipe_ingredients', 'recipe_id',)
    # readonly_fields = ['units']

    @admin.display(
        description='Рецепт',
    )
    def recipe_id(self, obj):
        return obj.recipe.id


admin.site.register(Tag)


class IngredientAdmin(admin.ModelAdmin):
    # inlines = (RecipeIngredientInline,)

    list_display = (
        'title', 'measurement_unit')
    list_filter = ('title',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Units)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
