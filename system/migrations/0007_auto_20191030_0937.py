# Generated by Django 2.1.7 on 2019-10-30 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20190918_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileattachments',
            name='spectra',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='distilledwaterloop',
            name='conductivity',
            field=models.FloatField(null=True, verbose_name='HCW-ST-101 Conduct. (uS)'),
        ),
        migrations.AlterField(
            model_name='distilledwaterloop',
            name='temperature',
            field=models.FloatField(null=True, verbose_name='HCW-TI-101 Temp (F)'),
        ),
    ]
