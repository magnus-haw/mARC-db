# Generated by Django 2.1.11 on 2021-04-23 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('units', '__first__'),
        ('data', '0027_auto_20210423_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alternateunitname',
            name='units',
        ),
        migrations.AddField(
            model_name='diagnosticcalibration',
            name='outputUnits',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='outputUnits', to='units.ComboUnit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='diagnosticcalibration',
            name='inputUnits',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputUnits', to='units.ComboUnit'),
        ),
        migrations.DeleteModel(
            name='AlternateUnitName',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
