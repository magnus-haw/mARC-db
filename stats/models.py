from django.db import models
from data.models import Run,Test
from data.stats import Nozzle, StingArm, CalType, CalShape

# Create your models here.
class ConditionAggregate(models.Model):
    name = models.CharField(max_length=200)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    value = models.FloatField(null=True,blank=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name

class IHFAggregate(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE,null=True,blank=True)
    arm = models.ForeignKey(StingArm, on_delete=models.CASCADE,null=True,blank=True)
    condition = models.CharField(max_length=15, null=True,blank=True)
    nozzle = models.ForeignKey(Nozzle, on_delete=models.CASCADE,null=True,blank=True)
    calsize = models.FloatField(verbose_name="CalSize [in]",null=True,blank=True)
    calshape= models.ForeignKey(CalShape, on_delete=models.CASCADE,null=True,blank=True)
    caltype = models.ForeignKey(CalType, on_delete=models.CASCADE,null=True,blank=True)
    standoff_dist = models.FloatField(verbose_name="Distance from NEP [in]",null=True,blank=True)
    winovich = models.FloatField(verbose_name="Winovich Sonic Enthalpy [MJ/kg]",null=True,blank=True)
    shepard = models.FloatField(verbose_name="Shepard Sonic Enthalpy [MJ/kg]",null=True,blank=True)
    eb2 = models.FloatField(verbose_name="EB2 [MJ/kg]",null=True,blank=True)
    eb2err = models.FloatField(verbose_name="EB2 err [%]",null=True,blank=True)
    dt41 = models.FloatField(verbose_name="DT41_0 [degC]",null=True,blank=True)
    dt41set = models.FloatField(verbose_name="DT41_0 set to [degC]",null=True,blank=True)
    arcEff = models.FloatField(verbose_name="Winovich Sonic Enthalpy [MJ/kg]",null=True,blank=True)
    hcenterline = models.FloatField(verbose_name="h_centerline [MJ/kg]",null=True,blank=True)
    qcenter = models.FloatField(verbose_name="q_center [W/cm^2]",null=True,blank=True)
    Pt2 = models.FloatField(verbose_name="P_t2 [kPa]",null=True,blank=True)
    arcpressure = models.FloatField(verbose_name="Arc pressure [kPa]",null=True,blank=True)
    arccurrent = models.FloatField(verbose_name="Arc current [A]",null=True,blank=True)
    arcvoltage = models.FloatField(verbose_name="Arc voltage [V]",null=True,blank=True)
    mainair = models.FloatField(verbose_name="Main air [g/s]",null=True,blank=True)
    addair = models.FloatField(verbose_name="Add air [g/s]",null=True,blank=True)
    argon = models.FloatField(verbose_name="Argon [g/s]",null=True,blank=True)
    reff = models.FloatField(verbose_name="R_eff [cm]",null=True,blank=True)
    qreff= models.FloatField(verbose_name="qR_eff [W/cm^1.5]",null=True,blank=True)
    comments = models.TextField(null=True,blank=True)
    tstart = models.FloatField(verbose_name="Start time [s]",null=True,blank=True)
    tend = models.FloatField(verbose_name="End time [s]",null=True,blank=True)
    boxpressure = models.FloatField(verbose_name="Box pressure [kPa]",null=True,blank=True)

