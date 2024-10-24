# Generated by Django 4.2.11 on 2024-10-24 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pragmatic', '0010_sitesetting'),
        ('slots', '0031_slot_context'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('value', models.TextField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pragmatic.provider')),
            ],
            options={
                'unique_together': {('provider', 'name')},
            },
        ),
    ]
