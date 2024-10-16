# Generated by Django 4.2.11 on 2024-10-02 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0064_alter_sites_casino'),
    ]

    operations = [
        migrations.AddField(
            model_name='sites',
            name='slot_rtp',
            field=models.CharField(blank=True, default='98.96', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sites',
            name='author',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.author'),
        ),
    ]
