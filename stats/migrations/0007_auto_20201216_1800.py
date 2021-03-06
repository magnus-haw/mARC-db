# Generated by Django 2.1.11 on 2020-12-17 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0020_run_flag'),
        ('system', '0022_auto_20201211_2305'),
        ('stats', '0006_linearmodel_fit_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticConditionAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('err', models.FloatField(blank=True, null=True)),
                ('npoints', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(null=True)),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.Condition')),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Diagnostic')),
            ],
        ),
        migrations.RenameField(
            model_name='linearmodel',
            old_name='created_at',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='linearmodel',
            old_name='updated_at',
            new_name='updated',
        ),
        migrations.AddField(
            model_name='seriesstartupstats',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
