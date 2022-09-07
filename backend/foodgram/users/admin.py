from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ShoppingCartByUser, SubscribersByCurrentUser
from foods.models import FavoritedRecipesByUsers


@admin.register(FavoritedRecipesByUsers)
class FavoritedRecipesByUsersAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'recipe')


@admin.register(ShoppingCartByUser)
class ShoppingCartByUserAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'recipe')


@admin.register(SubscribersByCurrentUser)
class SubscribersByCurrentUserAdmin(admin.ModelAdmin):
    list_display = (
        'current_user', 'subscription')


UserAdmin.list_filter = ('email', 'first_name',
                         'last_name', 'username')
