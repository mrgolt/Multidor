# Generated by Django 4.2.11 on 2024-10-06 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pragmatic', '0004_site_offers'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='home_template',
            field=models.CharField(blank=True, choices=[], max_length=255),
        ),
    ]