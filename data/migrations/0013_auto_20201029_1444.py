# Generated by Django 2.1.11 on 2020-10-29 21:44

import data.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_auto_20190917_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', data.models.MyArrayField()),
                ('name', models.CharField(max_length=150)),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Diagnostic')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Run')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', data.models.MyArrayField()),
            ],
        ),
        migrations.AlterField(
            model_name='series',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AddField(
            model_name='diagnosticseries',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.TimeSeries'),
        ),
    ]
