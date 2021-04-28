from django.db import models
import pandas as pd
import numpy as np

from units.models import ComboUnit
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=50,unique=True)
    notes= models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "People"

class Apparatus(models.Model):
    name = models.CharField(max_length=200,unique=True)
    acronym = models.CharField(max_length=10,unique=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']
        verbose_name_plural = "Apparatus"

class Test(models.Model):
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
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    test_engineer = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL,related_name = "test_engineer")
    principle_investigator = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL, related_name = "principle_investigator")
    operator = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL,related_name = "operator")
    objective = models.TextField(null=True,blank=True)
    procedure = models.TextField(null=True,blank=True)
    nozzle = models.ForeignKey('system.Nozzle',null=True,on_delete=models.SET_NULL)
    cathode = models.ForeignKey('system.Cathode', on_delete=models.SET_NULL, null=True)
    disks = models.ManyToManyField('system.Disk', blank=True)
    diagnostics = models.ManyToManyField('Diagnostic')
    notes = models.TextField(null=True,blank=True)
    
    class Meta:
        unique_together = (("name", "test"),)
        ordering = ['-date']
    
    def __str__(self):
        return self.name

    # def get_dataframe(self):
    #     series = Series.objects.filter(run=self)
    #     col_data, col_names = [],[]
    #     for s in series:
    #         col_names.append(s.diagnostic.name)
    #         col_data.append( s.record_set.order_by('index').values_list('value',flat=True) )
    #     d = np.array( col_data ).T
    #     return pd.DataFrame(d,columns=col_names)

    def get_dataframe(self):
        series = DiagnosticSeries.objects.filter(run=self)
        col_data, col_names = [],[]
        timelabel = "Time [s]"

        ### Check if more than one time series
        q_ts = TimeSeries.objects.filter(diagnosticseries__run =self).distinct()
        if len(q_ts)==1:
            col_names.append(timelabel)
            col_data.append(q_ts[0].time)
            for s in series:
                col_names.append(s.diagnostic.name)
                col_data.append( s.values )
        else:
            for s in series:
                col_names.append(timelabel)
                col_data.append( s.time.time )
                col_names.append(s.diagnostic.name)
                col_data.append( s.values )
        d = np.array( col_data ).T
        
        return pd.DataFrame(d,columns=col_names)
        
    def get_diagnostics(self):
        dg_list = DiagnosticSeries.objects.filter(run=self).values_list('diagnostic__name',flat=True)
        diagnostics = Diagnostic.objects.filter(name__in=dg_list,apparatus=self.test.apparatus)
        return diagnostics

class Diagnostic(models.Model):
    name = models.CharField(max_length=50)
    units = models.ForeignKey(ComboUnit, on_delete=models.CASCADE)
    apparatus = models.ForeignKey(Apparatus, on_delete=models.CASCADE)
    notes = models.TextField(blank=True,null=True)
    sensor= models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    datasheet = models.FileField(null=True, blank=True)
    flag_if_missing = models.BooleanField(null=True, blank=True, default=False)
    is_input_setting = models.BooleanField(default=False)

    DATATYPES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('XT','Time series'),
        ('XYT', 'N-dim time series'),
        ('LIDAR', 'Point cloud'),
        ('OTHER', 'Other'),
    ]

    TYPES = [
        ('SYSTEM', 'System'),
        ('ENVIRN', 'Environmental'),
        ('CAMERA', 'Camera'),
        ('INSERT', 'Insertion'),
        ('OTHER', 'Other'),
    ]
    category = models.CharField(
        max_length=6,
        choices=TYPES,
        default='SYSTEM',
    )

    datatype = models.CharField(
        max_length=6,
        choices=DATATYPES,
        default='XT',
    )
    
    def __str__(self):
        return self.name

class AlternateDiagnosticName(models.Model):
    name = models.CharField(max_length=50)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)

class MyArrayField(models.TextField):
    description = "A numpy array field serialized to txt"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return None
        elif isinstance(value, np.ndarray):
            return value
        else:
            return np.fromstring(value, sep=' ')

    def get_prep_value(self, value):
        if value is None:
            return None
        else:
            strrep = np.array2string(value,threshold=np.inf,max_line_width=np.inf)
            return strrep[1:-1]

class TimeSeries(models.Model):
    time = MyArrayField()

class DiagnosticCalibration(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    vinput = MyArrayField()
    inputUnits = models.ForeignKey(ComboUnit, on_delete=models.CASCADE, related_name="inputUnits")
    output = MyArrayField()
    outputUnits = models.ForeignKey(ComboUnit, on_delete=models.CASCADE, related_name="outputUnits")
    resolution = models.FloatField(blank=True,null=True)
    temporalresolution = models.FloatField(blank=True,null=True)
    
    description = models.TextField()
    date = models.DateTimeField(null=True)
    expiration = models.DateField(null=True)
    datasheet = models.FileField(null=True, blank=True)

    def calibrate(self,vin):
        cal = np.interp(vin, self.vinput,self.output, left=np.nan, right=np.nan)
        return cal

class DiagnosticSetup(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    expiration = models.DateField(null=True, blank=True)
    description = models.TextField()
    components = models.ManyToManyField("system.component", blank=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.diagnostic.name + str(self.date)

class DiagnosticSeries(models.Model):
    time = models.ForeignKey(TimeSeries, on_delete=models.CASCADE)
    values = MyArrayField()
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def interp(self, tnew):
        ###!!! interpolate values uniformly without nans.
        t0,vals = self.time.time, self.values
        nans = np.isnan(vals)
        return np.interp(tnew, t0[~nans], vals[~nans])

class DiagnosticFile(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    file = models.FileField()

    DOCUMENT = 'DOC'
    IMAGE = 'IMG'
    VIDEO = 'VID'
    OTHER = 'OTR'
    FILETYPES = [
        (DOCUMENT, 'Document'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (OTHER, 'Other'),
    ]
    type = models.CharField(
        max_length=3,
        choices=FILETYPES,
        default=DOCUMENT,
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural="diagnostic files"