# Generated by Django 4.2.11 on 2024-05-03 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0044_symbol_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('short_bio', models.TextField(blank=True, default='')),
                ('bio', models.TextField(blank=True, default='')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='authors/')),
                ('position', models.CharField(max_length=500)),
            ],
        ),
    ]
