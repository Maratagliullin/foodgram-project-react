# Generated by Django 4.1 on 2022-09-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_favoritedrecipesbyusers'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoritedrecipesbyusers',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='ingredient',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='favoritedrecipesbyusers',
            constraint=models.UniqueConstraint(fields=('current_user', 'recipe'), name='unique_current_current_recipe'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('title', 'measurement_unit'), name='unique_title_measurement_unit'),
        ),
    ]
