# Generated by Django 4.2.11 on 2024-04-02 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0022_alter_click_date_clicked'),
    ]

    operations = [
        migrations.AddField(
            model_name='sites',
            name='template_name',
            field=models.CharField(blank=True, default='main.html', max_length=200),
        ),
    ]
