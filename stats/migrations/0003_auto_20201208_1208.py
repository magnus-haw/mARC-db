# Generated by Django 2.1.11 on 2020-12-08 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_conditioninstanceflag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conditioninstanceflag',
            name='instance',
        ),
        migrations.AlterField(
            model_name='seriesstablestats',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.ConditionInstanceFit'),
        ),
        migrations.AlterField(
            model_name='seriesstartupstats',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.ConditionInstanceFit'),
        ),
        migrations.DeleteModel(
            name='ConditionInstanceFlag',
        ),
    ]
