# Generated by Django 4.2.11 on 2024-05-03 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0045_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='sites',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.author'),
        ),
    ]