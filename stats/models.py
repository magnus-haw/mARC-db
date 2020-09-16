from django.db import models
from data.models import Run,Diagnostic
from system.models import Condition, ConditionInstance

# Create your models here.
class ConditionAggregate(models.Model):
    instance = models.ForeignKey(ConditionInstance, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    avg = models.FloatField(null=True,blank=True)
    stdev = models.FloatField(null=True,blank=True)
    min   = models.FloatField(null=True,blank=True)
    max   = models.FloatField(null=True,blank=True)
