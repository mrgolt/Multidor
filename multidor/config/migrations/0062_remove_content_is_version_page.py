# Generated by Django 4.2.11 on 2024-09-28 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0061_content_demo_content_is_version_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='is_version_page',
        ),
    ]