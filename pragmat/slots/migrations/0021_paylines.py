# Generated by Django 4.2.11 on 2024-10-13 11:58

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0020_feature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paylines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('russian_title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True)),
            ],
        ),
    ]