# Generated by Django 4.2.11 on 2024-10-06 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pragmatic', '0005_site_home_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='home_template',
            field=models.CharField(default='home.html', max_length=255),
        ),
    ]
