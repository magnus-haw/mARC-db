# Generated by Django 2.1 on 2018-09-06 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sheet',
            unique_together={('name', 'spreadsheet')},
        ),
    ]