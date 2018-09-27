# Generated by Django 2.1.1 on 2018-09-26 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20180926_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='avg_current',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sheet',
            name='avg_plasma_gas',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sheet',
            name='avg_shield_gas',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sheet',
            name='avg_voltage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
