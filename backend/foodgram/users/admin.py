from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (FavoritedRecipesByUser, ShoppingCartByUser,
                     SubscribersByCurrentUser)


class FavoritedRecipesByUserAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'recipe')

    def in_favorites(self, obj):
        return FavoritedRecipesByUser.objects.filter(recipe=obj).count()


admin.site.register(FavoritedRecipesByUser, FavoritedRecipesByUserAdmin)


class ShoppingCartByUserAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'recipe')


admin.site.register(ShoppingCartByUser, ShoppingCartByUserAdmin)


class SubscribersByCurrentUserAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'subscription')


admin.site.register(SubscribersByCurrentUser, SubscribersByCurrentUserAdmin)


UserAdmin.list_filter = ('email', 'first_name',
                         'last_name', 'username')
