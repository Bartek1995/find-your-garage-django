# Generated by Django 4.0.6 on 2022-10-06 15:40

import django.core.validators
from django.db import migrations, models
import garages.validators


class Migration(migrations.Migration):

    dependencies = [
        ('garages', '0006_alter_garage_nip_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garage',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[garages.validators.validate_poland_country], verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='garage',
            name='name',
            field=models.CharField(blank=True, max_length=50, validators=[garages.validators.validate_special_characters], verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='garage',
            name='nip_number',
            field=models.BigIntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(9999999999, message='Niepoprawny numer NIP'), django.core.validators.MinValueValidator(1000000000, message='Niepoprawny numer NIP')], verbose_name='NIP Number'),
        ),
        migrations.AlterField(
            model_name='garage',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code'),
        ),
    ]