# Generated by Django 4.1 on 2022-09-07 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_alter_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ingredients', to='foods.units', verbose_name='Единица изменения'),
        ),
    ]
