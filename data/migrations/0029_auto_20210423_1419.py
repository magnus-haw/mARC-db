# Generated by Django 2.1.11 on 2021-04-23 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0036_auto_20210422_2224'),
        ('data', '0028_auto_20210423_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='datatype',
            field=models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('XT', 'Time series'), ('XYT', 'N-dim time series'), ('LIDAR', 'Point cloud'), ('OTHER', 'Other')], default='XT', max_length=6),
        ),
        migrations.AddField(
            model_name='diagnostic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='diagnostic',
            name='is_input_setting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='diagnosticsetup',
            name='components',
            field=models.ManyToManyField(blank=True, to='system.Component'),
        ),
        migrations.AlterField(
            model_name='diagnostic',
            name='category',
            field=models.CharField(choices=[('SYSTEM', 'System'), ('ENVIRN', 'Environmental'), ('CAMERA', 'Camera'), ('INSERT', 'Insertion'), ('OTHER', 'Other')], default='SYSTEM', max_length=6),
        ),
    ]
