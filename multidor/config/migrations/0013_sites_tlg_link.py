# Generated by Django 4.2.11 on 2024-03-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0012_remove_content_yt_link_sites_yt_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='sites',
            name='tlg_link',
            field=models.TextField(blank=True, default='https://t.me/play_sweet_bonanza'),
        ),
    ]
