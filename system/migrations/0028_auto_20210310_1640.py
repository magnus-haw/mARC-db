# Generated by Django 2.1.11 on 2021-03-11 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0027_auto_20210301_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='gas',
            name='ionization_energy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gas',
            name='molecular_weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
