# Generated by Django 2.1.1 on 2018-09-27 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_auto_20180926_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apparatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('notes', models.TextField(null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('notes', models.TextField(null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
