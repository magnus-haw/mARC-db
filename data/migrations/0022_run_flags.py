# Generated by Django 2.1.11 on 2021-02-12 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0021_remove_run_flag'),
        ('stats', '0008_flag_runusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='flags',
            field=models.ManyToManyField(blank=True, to='stats.Flag'),
        ),
    ]