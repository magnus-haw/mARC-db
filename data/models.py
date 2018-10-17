from django.db import models
import pandas as pd
from numpy import array,shape
# Create your models here.

class Facility(models.Model):
    name = models.CharField(max_length=200,unique=True)
    acronym = models.CharField(max_length=10,unique=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']
        verbose_name_plural = "Facilities"

class Apparatus(models.Model):
    name = models.CharField(max_length=200,unique=True)
    acronym = models.CharField(max_length=10,unique=True)
    notes = models.TextField(null=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']
        verbose_name_plural = "Apparatus"

class Experiment(models.Model):
    name = models.CharField(max_length=200,unique=True)
    date = models.DateField()
    notes = models.TextField(null=True)
    apparatus = models.ForeignKey(Apparatus, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date']

class Run(models.Model):
    name = models.CharField(max_length=200)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    start_index = models.IntegerField(null=True,blank=True)
    end_index = models.IntegerField(null=True,blank=True)
    avg_current = models.FloatField(null=True,blank=True)
    std_current = models.FloatField(null=True,blank=True)
    avg_voltage = models.FloatField(null=True,blank=True)
    avg_plasma_gas = models.FloatField(null=True,blank=True)
    avg_shield_gas = models.FloatField(null=True,blank=True)
    avg_chamber_pressure = models.FloatField(null=True,blank=True)
    avg_column_pressure = models.FloatField(null=True,blank=True)
    
    notes = models.TextField(null=True)
    
    class Meta:
        unique_together = (("name", "experiment"),)
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def get_dataframe(self):
        series = Series.objects.filter(run=self)
        col_data, col_names = [],[]
        for s in series:
            col_names.append(s.name)
            col_data.append( s.record_set.order_by('index').values_list('value',flat=True) )
        d = array( col_data ).T
        return pd.DataFrame(d,columns=col_names)
        
    def get_diagnostics(self):
        dg_list = Series.objects.filter(run=self).values_list('diagnostic__name',flat=True)
        diagnostics = Diagnostic.objects.filter(name__in=dg_list)
        return diagnostics

class RunAggregate(models.Model):
    name = models.CharField(max_length=200)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    value = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)
    user = models.ForeignKey('auth.User',null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50,unique=True)
    short_name = models.CharField(max_length=5,unique=True)
    def __str__(self):
        return self.name

class AlternateUnitName(models.Model):
    name = models.CharField(max_length=50,unique=True)
    units = models.ForeignKey(Unit, on_delete=models.CASCADE)

class Diagnostic(models.Model):
    name = models.CharField(max_length=50,unique=True)
    units = models.ForeignKey(Unit, on_delete=models.CASCADE)
    apparatus = models.ForeignKey(Apparatus, on_delete=models.CASCADE)
    notes = models.TextField(blank=True,null=True)
    sensor= models.CharField(max_length=200)
    description = models.TextField()
    resolution = models.FloatField(blank=True,null=True)
    noise = models.FloatField(blank=True,null=True)
    
    def __str__(self):
        return self.name

class AlternateDiagnosticName(models.Model):
    name = models.CharField(max_length=50,unique=True)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)

class Series(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Series"

class Record(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    value = models.FloatField(null=True,blank=True)
    index = models.IntegerField(editable=False)
