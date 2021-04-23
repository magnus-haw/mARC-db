from django.db import models
from data.models import Run, Diagnostic, DiagnosticSeries, TimeSeries, MyArrayField
from system.models import ConditionInstance, Condition
from sklearn import linear_model

# Create your models here.

class ConditionInstanceFit(models.Model):
    instance = models.OneToOneField(ConditionInstance, on_delete=models.CASCADE)
    start = models.FloatField(null=True,blank=True)
    stable_start = models.FloatField(null=True,blank=True)
    stable_end = models.FloatField(null=True,blank=True)
    end = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.instance.name + "_" + str(self.start) + "_" + str(self.end)

class RunUsage(models.Model):
    run = models.OneToOneField(Run, on_delete=models.CASCADE)
    time = models.FloatField(null=True,blank=True)
    energy = models.FloatField(null=True,blank=True)
    mass = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.run.name + "_use_stats"

class DiagnosticConditionAverage(models.Model):
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    value = models.FloatField(null=True, blank=True)
    err = models.FloatField(null=True, blank=True)
    npoints = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.condition.name + "_" + str(self.diagnostic) + "_" + str(self.value)

class SeriesStableStats(models.Model):
    series = models.ForeignKey(DiagnosticSeries, on_delete=models.CASCADE)
    condition = models.ForeignKey(ConditionInstanceFit, on_delete=models.CASCADE)
    avg = models.FloatField(null=True,blank=True)
    stdev = models.FloatField(null=True,blank=True)
    min = models.FloatField(null=True,blank=True)
    max = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.series.diagnostic.name + "_" + self.condition.instance.run.name + "_" + self.condition.instance.run.test.name

class SeriesStartupStats(models.Model):
    series = models.ForeignKey(DiagnosticSeries, on_delete=models.CASCADE)
    condition = models.ForeignKey(ConditionInstanceFit, on_delete=models.CASCADE)
    dt = models.FloatField(null=True,blank=True)
    stdev = models.FloatField(null=True,blank=True)
    min = models.FloatField(null=True,blank=True)
    max = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.series.diagnostic.name + "_" + self.condition.instance.run.name + "_" + self.condition.instance.run.test.name


class MyListField(models.TextField):
    description = "A string list serialized to txt"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return None
        elif isinstance(value, list):
            return value
        else:
            return eval(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        else:
            strrep = repr(value)
            return strrep

class LinearModel(models.Model):
    name = models.CharField(max_length=150)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, null=True,blank=True)
    headers = MyListField(null=True,blank=True)
    coeff = MyArrayField(null=True,blank=True)
    intercept = models.FloatField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fit_method = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name + "_" + str(self.updated)

    def getModelObject(self):
        reg = linear_model.LinearRegression()
        reg.coef_ = self.coeff
        reg.intercept_ = self.intercept
        return reg


class Flag(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    FLAGTYPES = [
        (0, 'Missing diagnostic'),
        (1, 'Missing input diagnostic'),
        (2, 'Run aborted'),
        (3, 'Arc unstable'),
        (4, 'Water leak'),
        (5, 'Insufficient vacuum'),
    ]
    rating = models.PositiveIntegerField(default=0, choices=FLAGTYPES)
    description = models.CharField(max_length=150, null=True, blank=True)
    
    def __str__(self):
        return self.rating + "_" + self.description  
