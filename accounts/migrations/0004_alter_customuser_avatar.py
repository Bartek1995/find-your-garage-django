# Generated by Django 4.0.6 on 2022-10-30 23:14

from django.db import migrations, models
import myproject.azure_blob_storage


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=myproject.azure_blob_storage.OverwriteStorage(), upload_to=''),
        ),
    ]
