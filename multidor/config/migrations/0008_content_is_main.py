# Generated by Django 4.2.11 on 2024-03-13 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0007_sites_provider_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='is_main',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
