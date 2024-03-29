# Generated by Django 4.0.6 on 2022-11-01 22:32

import cars.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_alter_car_body_type_alter_car_engine_capacity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='production_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Rok produkcji'),
        ),
        migrations.AlterField(
            model_name='car',
            name='vin_number',
            field=models.CharField(blank=True, max_length=17, validators=[cars.validators.validate_vin], verbose_name='Numer VIN'),
        ),
    ]
