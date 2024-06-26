# Generated by Django 4.2.11 on 2024-03-26 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0019_bonus_is_active_bonus_redirect_casino_redirect_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='redirect',
            name='visits',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='casino',
            name='redirect',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='config.redirect'),
        ),
    ]
