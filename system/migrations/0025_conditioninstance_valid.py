# Generated by Django 2.1.11 on 2020-12-18 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0024_condition_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditioninstance',
            name='valid',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]