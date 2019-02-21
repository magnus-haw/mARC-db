from django.db import models
import pandas as pd
from numpy import array,shape
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50,unique=True)
    notes= models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

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

class Gas(models.Model):
    name = models.CharField(max_length=200,unique=True)
    abbrv = models.CharField(max_length=6,null=True,blank=True,unique=True)
    notes = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class StingDevice(models.Model):
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    limits = models.CharField(max_length=200)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name

class Run(models.Model):
    name = models.CharField(max_length=200)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    test_engineer = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL,related_name = "test_engineer")
    principle_investigator = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL, related_name = "principle_investigator")
    operator = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL,related_name = "operator")
    objective = models.TextField(null=True)
    nozzle_exit_diameter = models.FloatField(null=True)
    total_cathode_time = models.FloatField(null=True)
    total_arc_on_duration = models.FloatField(null=True)
    number_disks = models.PositiveSmallIntegerField(null=True,default=3)
    number_cathode_starts = models.PositiveIntegerField(null=True,default=1)
    
    
    main_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL, related_name = "main_gas")
    shield_gas =models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL,related_name = "shield_gas")
    purge_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL,related_name = "purge_gas")
    
    procedure = models.TextField(null=True)
    swivel_sting_arm = models.ForeignKey(StingDevice, null=True, blank=True, on_delete=models.SET_NULL,related_name = "stingsw")
    L1_sting_arm = models.ForeignKey(StingDevice, null=True, blank=True, on_delete=models.SET_NULL,related_name = "L1")
    L2_sting_arm = models.ForeignKey(StingDevice, null=True, blank=True, on_delete=models.SET_NULL,related_name = "L2")
    
    pretest_photo = models.ImageField(null=True,blank=True)
    posttest_photo= models.ImageField(null=True,blank=True)
    video = models.FileField(null=True,blank=True)
    
    notes = models.TextField(null=True,blank=True)
    
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
