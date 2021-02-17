# Generated by Django 2.1.11 on 2021-02-12 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0021_remove_run_flag'),
        ('stats', '0007_auto_20201216_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RunUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.FloatField(blank=True, null=True)),
                ('energy', models.FloatField(blank=True, null=True)),
                ('mass', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(null=True)),
                ('run', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data.Run')),
            ],
        ),
    ]
