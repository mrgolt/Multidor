# Generated by Django 4.2.11 on 2024-10-06 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0012_slot_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]