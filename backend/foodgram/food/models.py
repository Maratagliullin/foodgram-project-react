from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Теги"""

    name = models.CharField('Название', max_length=200, unique=True)
    slug = models.SlugField('Слуг', unique=True)
    color = ColorField(
        'Цвет', default='#FF0000')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Units(models.Model):
    """Единицы измерения"""

    title = models.CharField(verbose_name='Название',
                             max_length=500, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Идиница измерения'
        verbose_name_plural = 'Единицы измерения'


class Ingredient(models.Model):
    """Ингредиенты"""

    title = models.CharField('Название', max_length=500)
    measurement_unit = models.ForeignKey(
        Units,
        on_delete=models.SET_NULL, null=True,
        related_name='ingredients',
        verbose_name='Единица изменения'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        unique_together = ['title', 'measurement_unit']


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
        upload_to='food/',
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name="Тег")
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
        verbose_name="Ингредиенты")
    time = models.IntegerField(verbose_name='Время приготовления',
                               help_text='Время приготовления в минутах',
                               )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


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

    def __str__(self):
        return str(self.recipe)
