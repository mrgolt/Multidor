# Generated by Django 4.2.13 on 2024-11-20 07:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0070_alter_sites_css_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='casino',
            name='alternative_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='casino',
            name='logo_svg',
            field=models.FileField(default='logo.svg', upload_to='img/', validators=[django.core.validators.FileExtensionValidator(['svg', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='sites',
            name='css_file',
            field=models.FileField(blank=True, default='css/dark.min.css', upload_to='css/'),
        ),
    ]