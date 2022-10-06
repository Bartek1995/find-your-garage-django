# Generated by Django 4.0.6 on 2022-10-05 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garages', '0005_alter_garage_nip_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garage',
            name='nip_number',
            field=models.BigIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1000000000)], verbose_name='NIP Number'),
        ),
    ]
