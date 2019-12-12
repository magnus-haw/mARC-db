from django.db import models

# Create your models here.
class ConditionAggregate(models.Model):
    name = models.CharField(max_length=200)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    value = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name
