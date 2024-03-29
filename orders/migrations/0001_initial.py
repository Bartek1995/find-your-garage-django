# Generated by Django 4.0.6 on 2022-12-04 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('garages', '0015_alter_garage_name_alter_openinghours_from_hour_and_more'),
        ('cars', '0009_car_date_of_expiry_of_insurance_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.PositiveSmallIntegerField(choices=[(1, 'Oczekujące na akceptację'), (2, 'Zaakceptowane'), (3, 'W trakcie realizacji'), (4, 'Zrealizowane'), (5, 'Odrzucone'), (6, 'Wstrzymane'), (7, 'Oczekiwanie na akceptacje zmian')], default=1, verbose_name='Status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Data modyfikacji')),
                ('description', models.TextField(blank=True, verbose_name='Opis')),
                ('car', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.car')),
                ('garage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='garages.garage')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_expenditure', models.CharField(choices=[(1, 'Części'), (2, 'Usługa'), (3, 'Inne')], max_length=10, verbose_name='Typ wydatku')),
                ('name', models.CharField(max_length=50, verbose_name='Nazwa wydatku')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cena')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cars.car')),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
