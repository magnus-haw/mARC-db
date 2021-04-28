# Generated by Django 2.1.11 on 2021-04-23 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0035_auto_20210422_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsystemconfigitem',
            name='value1_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='val1unit', to='units.ComboUnit'),
        ),
        migrations.AlterField(
            model_name='subsystemconfigitem',
            name='value2_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='val2unit', to='units.ComboUnit'),
        ),
    ]
