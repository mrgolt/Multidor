# Generated by Django 4.2.11 on 2024-04-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0037_faq_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='type',
            field=models.CharField(default='CPA', max_length=100),
        ),
    ]