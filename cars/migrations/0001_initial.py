# Generated by Django 4.0.6 on 2022-10-30 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=50, verbose_name='Marka')),
                ('model', models.CharField(blank=True, max_length=50, verbose_name='Model')),
                ('vin_number', models.CharField(blank=True, max_length=17, verbose_name='Numer VIN')),
                ('engine_capacity', models.DecimalField(blank=True, decimal_places=3, max_digits=4, verbose_name='Pojemność silnika')),
                ('production_year', models.IntegerField(blank=True, verbose_name='Rok produkcji')),
                ('engine_type', models.CharField(blank=True, choices=[('PB', 'Benzyna'), ('PB+LPG', 'Benzyna + LPG'), ('ON', 'Diesel'), ('HYB', 'Hybryda'), ('ELE', 'Elektryczny'), ('OTHER', 'Inny')], max_length=50, verbose_name='Rodzaj silnika')),
                ('gearbox_type', models.CharField(blank=True, choices=[('manual', 'Manualna'), ('automatic', 'Automatyczna'), ('semi-automatic', 'Półautomatyczna')], max_length=50, verbose_name='Rodzaj skrzyni biegów')),
                ('engine_power', models.IntegerField(blank=True, verbose_name='Moc silnika')),
                ('body_type', models.CharField(blank=True, choices=[('Hatchback', 'Hatchback'), ('Combi', 'Combi'), ('Sedan', 'Sedan'), ('Coupe', 'Coupe'), ('Cabriollet', 'Kabriolet'), ('SUV', 'SUV'), ('Van', 'Van'), ('Pickup', 'Pickup')], max_length=50, verbose_name='Typ nadwozia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
