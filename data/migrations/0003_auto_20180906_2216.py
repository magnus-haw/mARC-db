# Generated by Django 2.1 on 2018-09-06 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20180906_2213'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='record',
            unique_together={('sheet', 'spreadsheet', 'time')},
        ),
    ]
