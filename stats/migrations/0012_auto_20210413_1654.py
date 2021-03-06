# Generated by Django 2.1.11 on 2021-04-13 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_auto_20210310_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='aborted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='flag',
            name='rating',
            field=models.PositiveIntegerField(choices=[(0, 'Missing diagnostic'), (1, 'Missing input diagnostic'), (2, 'Arc unstable'), (3, 'Water leak'), (4, 'Insufficient vacuum')], default=0),
        ),
    ]
