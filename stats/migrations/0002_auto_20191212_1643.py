# Generated by Django 2.2.5 on 2019-12-13 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ihfaggregate',
            options={'ordering': ['test'], 'verbose_name': 'IHF Aggregate', 'verbose_name_plural': 'IHF Aggregates'},
        ),
    ]
