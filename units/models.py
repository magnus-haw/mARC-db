from django.db import models

# Create your models here.

class FundamentalUnit(models.Model):
    name = models.CharField(max_length=15)
    symbol = models.CharField(max_length=4)
    property = models.CharField(max_length=25)

    def __str__(self):
        return "["+self.symbol+"]"

class BaseUnit(models.Model):
    name = models.CharField(max_length=15)
    symbol = models.CharField(max_length=4)
    SI_unit = models.ForeignKey(FundamentalUnit,on_delete=models.CASCADE)
    SI_ratio = models.FloatField()

    def __str__(self):
        return self.symbol

class UnitPower(models.Model):
    unit = models.ForeignKey(BaseUnit,on_delete=models.CASCADE)
    power = models.IntegerField()

    def __str__(self):
        return self.symbol+"^"+str(self.power)

    def SI_symbol(self):
        "("+ self.unit.SI_unit.symbol+"^"+str(self.power)+ ")"

    def SI_ratio(self):
        (self.unit.SI_ratio)**self.power

class Unit(models.Model):
    name = models.CharField(max_length=15)
    symbol = models.CharField(max_length=4)
    unit_powers = models.ManyToManyField(UnitPower)

    def __str__(self):
        self.symbol

    def SI_ratio(self):
        ratio = 1
        for u in self.unit_powers.all():
            ratio *= u.SI_ratio()
        return ratio

    def SI_symbol(self):
        sym = ""
        for u in self.unit_powers.all():
            sym += u.SI_symbol()
        return sym