# Generated by Django 4.2.11 on 2024-09-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0053_casino_logo_svg'),
    ]

    operations = [
        migrations.AddField(
            model_name='sites',
            name='type',
            field=models.CharField(choices=[('slot', 'Slot'), ('casino', 'Casino')], default='slot', max_length=10),
        ),
    ]
