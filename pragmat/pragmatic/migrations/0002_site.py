# Generated by Django 4.2.11 on 2024-10-06 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pragmatic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pragmatic.provider')),
            ],
        ),
    ]
