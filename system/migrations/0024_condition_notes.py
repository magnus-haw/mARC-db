# Generated by Django 2.1.11 on 2020-12-17 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0023_condition_disks'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
