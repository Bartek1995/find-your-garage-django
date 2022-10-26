# Generated by Django 4.0.6 on 2022-10-26 14:46

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('garages', '0008_alter_garage_country_alter_garage_full_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garage',
            name='name',
            field=models.CharField(blank=True, max_length=50, validators=[main.validators.validate_special_characters_and_numbers], verbose_name='Name'),
        ),
    ]
