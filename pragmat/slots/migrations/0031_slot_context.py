# Generated by Django 4.2.11 on 2024-10-21 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0030_remove_feature_title_remove_paylines_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='context',
            field=models.TextField(blank=True),
        ),
    ]
