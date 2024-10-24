# Generated by Django 4.2.11 on 2024-10-03 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0066_casino_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casino',
            name='favicon',
            field=models.FileField(default='favicon.ico', upload_to='favicons/', validators=[django.core.validators.FileExtensionValidator(['ico', 'png', 'svg'])]),
        ),
    ]
