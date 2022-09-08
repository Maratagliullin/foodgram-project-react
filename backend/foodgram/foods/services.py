from django.db.models import Sum


def download_shopping_cart(request):

    all_recipe_in_shopping_cart = (
        request.user.user_to_shopping_cart.values(
            'recipe__ingredient__title',
            'recipe__ingredient__measurement_unit__title',
            'recipe__recipeingredient__amount'))

    all_recipe_in_shopping_cart = all_recipe_in_shopping_cart.values(
        'recipe__ingredient__title',
        'recipe__ingredient__measurement_unit__title').annotate(
        recipe__recipeingredient__amount=(
            Sum('recipe__recipeingredient__amount')))

    result_string = ''
    for item in all_recipe_in_shopping_cart:
        name = item['recipe__ingredient__title']
        measurement_title = (
            item['recipe__ingredient__measurement_unit__title'])
        amount = item['recipe__recipeingredient__amount']
        result_string += (
            f'{name} ({measurement_title}) — {amount} \n')

    return result_string
