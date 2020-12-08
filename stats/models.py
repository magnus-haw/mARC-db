from django.db import models
from data.models import Run, Diagnostic, DiagnosticSeries, TimeSeries
from system.models import ConditionInstance, Condition

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

class SeriesStableStats(models.Model):
    series = models.OneToOneField(DiagnosticSeries, on_delete=models.CASCADE)
    condition = models.ForeignKey(ConditionInstance, on_delete=models.CASCADE)
    avg = models.FloatField(null=True,blank=True)
    stdev = models.FloatField(null=True,blank=True)
    min = models.FloatField(null=True,blank=True)
    max = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.condition.condition + "_" + self.avg

class SeriesStartupStats(models.Model):
    series = models.OneToOneField(DiagnosticSeries, on_delete=models.CASCADE)
    condition = models.ForeignKey(ConditionInstance, on_delete=models.CASCADE)
    dt = models.FloatField(null=True,blank=True)
    stdev = models.FloatField(null=True,blank=True)
    min = models.FloatField(null=True,blank=True)
    max = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.condition.condition + "_" + self.dt

class ConditionInstanceFlag(models.Model):
    FAILED = 'FAILED'
    OFFNOMINAL = 'OFF-NOMINAL'
    SUCCESS = 'SUCCESS'
    OTHER = 'OTHER'
    CONDITIONFLAGS = [
        (FAILED, 'Failed'),
        (OFFNOMINAL, 'Off-nominal'),
        (SUCCESS, 'Success'),
        (OTHER, 'Other'),
    ]
    instance = models.ForeignKey(ConditionInstance, on_delete=models.CASCADE)
    valid = models.BooleanField(null=True,blank=True)
    flag = models.CharField(max_length=12,choices=CONDITIONFLAGS,null=True,blank=True)

    def __str__(self):
        return self.condition.condition + "_" + self.flag