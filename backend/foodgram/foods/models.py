from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Теги"""

    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('Слуг', unique=True)
    color = ColorField(
        'Цвет', default='#FF0000')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class MeasurementUnits(models.Model):
    """Единицы измерения"""

    title = models.CharField(verbose_name='Название',
                             max_length=50, unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """Ингредиенты, при удалении единицы измеренения(measurement_unit)
    установим null для всех ингреиентов
    у которых была удаленая единица измеренения"""

    title = models.CharField('Название', max_length=500)
    measurement_unit = models.ForeignKey(
        MeasurementUnits,
        on_delete=models.SET_NULL, null=True,
        related_name='ingredients',
        verbose_name='Единица изменения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'measurement_unit'],
                name='unique_title_measurement_unit'
            )
        ]

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """Рецепты"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание',)
    image = models.ImageField(
        'Картинка',
        upload_to='foods_images/',
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Тег')
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
        verbose_name='Ингредиенты')
    time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """Хранение рецептов"""

    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    recipe_ingredients = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Связь рецептов и игнредиентов'
        verbose_name_plural = 'Связь рецептов и игнредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'recipe_ingredients', 'amount'],
                name='unique_recipe_recipe_ingredients_amount'
            )
        ]

    def __str__(self):
        return str(self.recipe)


class FavoritedRecipesByUsers(models.Model):
    """Избранные рецепты пользователя"""

    current_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_to_favorited',
        verbose_name='Текущий пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Список избранного'
        constraints = [
            models.UniqueConstraint(
                fields=['current_user', 'recipe'],
                name='unique_current_current_recipe'
            )
        ]
