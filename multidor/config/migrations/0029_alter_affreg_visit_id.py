# Generated by Django 4.2.11 on 2024-04-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0028_rename_reg_date_affdep_dep_date_affdep_is_first'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affreg',
            name='visit_id',
            field=models.CharField(max_length=100),
        ),
    ]