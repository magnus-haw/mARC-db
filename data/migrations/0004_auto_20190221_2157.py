# Generated by Django 2.1.7 on 2019-02-21 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20180928_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('abbrv', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('notes', models.TextField(null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('notes', models.TextField(null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StingDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sn', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=200)),
                ('limits', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='apparatus',
            options={'ordering': ['pk'], 'verbose_name_plural': 'Apparatus'},
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'ordering': ['pk'], 'verbose_name_plural': 'Facilities'},
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'verbose_name_plural': 'Series'},
        ),
        migrations.RemoveField(
            model_name='run',
            name='avg_chamber_pressure',
        ),
        migrations.RemoveField(
            model_name='run',
            name='avg_column_pressure',
        ),
        migrations.RemoveField(
            model_name='run',
            name='avg_current',
        ),
        migrations.RemoveField(
            model_name='run',
            name='avg_plasma_gas',
        ),
        migrations.RemoveField(
            model_name='run',
            name='avg_shield_gas',
        ),
        migrations.RemoveField(
            model_name='run',
            name='avg_voltage',
        ),
        migrations.RemoveField(
            model_name='run',
            name='end_index',
        ),
        migrations.RemoveField(
            model_name='run',
            name='start_index',
        ),
        migrations.RemoveField(
            model_name='run',
            name='std_current',
        ),
        migrations.AddField(
            model_name='run',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='nozzle_exit_diameter',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='number_cathode_starts',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='number_disks',
            field=models.PositiveSmallIntegerField(default=3, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='objective',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='posttest_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='run',
            name='pretest_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='run',
            name='procedure',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='total_arc_on_duration',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='total_cathode_time',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='record',
            name='index',
            field=models.IntegerField(editable=False),
        ),
        migrations.AddField(
            model_name='run',
            name='L1_sting_arm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='L1', to='data.StingDevice'),
        ),
        migrations.AddField(
            model_name='run',
            name='L2_sting_arm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='L2', to='data.StingDevice'),
        ),
        migrations.AddField(
            model_name='run',
            name='main_gas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_gas', to='data.Gas'),
        ),
        migrations.AddField(
            model_name='run',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operator', to='data.Person'),
        ),
        migrations.AddField(
            model_name='run',
            name='principle_investigator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='principle_investigator', to='data.Person'),
        ),
        migrations.AddField(
            model_name='run',
            name='purge_gas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purge_gas', to='data.Gas'),
        ),
        migrations.AddField(
            model_name='run',
            name='shield_gas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shield_gas', to='data.Gas'),
        ),
        migrations.AddField(
            model_name='run',
            name='swivel_sting_arm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stingsw', to='data.StingDevice'),
        ),
        migrations.AddField(
            model_name='run',
            name='test_engineer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_engineer', to='data.Person'),
        ),
    ]
