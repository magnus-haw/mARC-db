# Generated by Django 2.1.11 on 2021-02-12 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0020_run_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='run',
            name='flag',
        ),
    ]
