# Generated by Django 4.0.6 on 2022-11-03 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_alter_car_engine_capacity_alter_car_production_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='engine_capacity',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Pojemność silnika'),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_power',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Moc silnika'),
        ),
    ]
