from django.db import models
from data.models import Run

# Create your models here.
class Gas(models.Model):
    name = models.CharField(max_length=200,unique=True)
    abbrv = models.CharField(max_length=6,null=True,blank=True,unique=True)
    notes = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "gases"

class StingDevice(models.Model):
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    size = models.CharField(max_length=200	)
    limits = models.CharField(max_length=200)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name

class VacuumWaterLoop(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    temperature = models.FloatField(verbose_name="HCW-ST-101 Temp (F)",null=True)
    conductivity= models.FloatField(verbose_name="HCW-ST-101 Conduct. (mS)",null=True)
    arc_supply_pressure = models.FloatField(verbose_name="HCW-PI-130 Arc supply (PSIG)",null=True)
    arc_return_pressure = models.FloatField(verbose_name="HCW-PI-133 Arc return (PSIG)",null=True)
    spare_supply_pressure = models.FloatField(verbose_name="HCW-PI-140 Spare supply (PSIG)",null=True)
    spare_return_pressure = models.FloatField(verbose_name="HCW-PI-146 Spare return (PSIG)",null=True)
    chamber_supply_pressure = models.FloatField(verbose_name="HCW-PI-147 Chamber supply (PSIG)",null=True)
    
class SensorWaterLoop(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    temperature = models.FloatField(verbose_name="HCW-ST-101 Temp (F)",null=True)
    conductivity= models.FloatField(verbose_name="HCW-ST-101 Conduct. (mS)",null=True)
    arc_supply_pressure = models.FloatField(verbose_name="HCW-PI-130 Arc supply (PSIG)",null=True)
    arc_return_pressure = models.FloatField(verbose_name="HCW-PI-133 Arc return (PSIG)",null=True)
    spare_supply_pressure = models.FloatField(verbose_name="HCW-PI-140 Spare supply (PSIG)",null=True)
    spare_return_pressure = models.FloatField(verbose_name="HCW-PI-146 Spare return (PSIG)",null=True)
    chamber_supply_pressure = models.FloatField(verbose_name="HCW-PI-147 Chamber supply (PSIG)",null=True)
    
class DistilledWaterLoop(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    temperature = models.FloatField(verbose_name="HCW-ST-101 Temp (F)",null=True)
    conductivity= models.FloatField(verbose_name="HCW-ST-101 Conduct. (mS)",null=True)
    arc_supply_pressure = models.FloatField(verbose_name="HCW-PI-130 Arc supply (PSIG)",null=True)
    arc_return_pressure = models.FloatField(verbose_name="HCW-PI-133 Arc return (PSIG)",null=True)
    spare_supply_pressure = models.FloatField(verbose_name="HCW-PI-140 Spare supply (PSIG)",null=True)
    spare_return_pressure = models.FloatField(verbose_name="HCW-PI-146 Spare return (PSIG)",null=True)
    chamber_supply_pressure = models.FloatField(verbose_name="HCW-PI-147 Chamber supply (PSIG)",null=True)

class VacuumSystem(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    pump_base_pressure = models.FloatField(verbose_name="pump base pressure GS-PI-381 (torr)",null=True)
    chamber_no_purge_pressure = models.FloatField(verbose_name="chamber no-purge pressure GS-PI-374 (torr)",null=True)
    chamber_purge_pressure = models.FloatField(verbose_name="chamber purge pressure (torr)",null=True)
    chamber_posttest_pressure = models.FloatField(verbose_name="chamber posttest pressure (torr)",null=True)
    
    
class GasSettings(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    plasma_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL, related_name = "plasma_gas")
    plasma_gas_initial_pressure = models.FloatField(verbose_name="plasma gas initial pressure (PSIG)",null=True,blank=True)
    plasma_gas_final_pressure = models.FloatField(verbose_name="plasma gas final pressure (PSIG)",null=True,blank=True)
    
    shield_gas =models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL,related_name = "shield_gas")
    shield_gas_initial_pressure = models.FloatField(verbose_name="shield gas initial pressure (PSIG)",null=True,blank=True)
    shield_gas_final_pressure = models.FloatField(verbose_name="shield gas final pressure (PSIG)",null=True,blank=True)

    purge_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL,related_name = "purge_gas")
    purge_gas_initial_pressure = models.FloatField(verbose_name="purge gas initial pressure (PSIG)",null=True,blank=True)
    purge_gas_final_pressure = models.FloatField(verbose_name="purge gas final pressure (PSIG)",null=True,blank=True)

    class Meta:
        verbose_name_plural="gas settings"

class HeaterSettings(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    nozzle_exit_diameter = models.FloatField(null=True,verbose_name="nozzle exit diameter (cm)")
    total_cathode_time = models.FloatField(null=True,verbose_name="total cathode time (s)")
    total_arc_on_duration = models.FloatField(null=True,verbose_name="total arc-on duration (s)")
    number_disks = models.PositiveSmallIntegerField(null=True,default=3)
    number_cathode_starts = models.PositiveIntegerField(null=True,default=1)
    class Meta:
        verbose_name_plural="heater settings"

class StingSettings(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    swivel_sting_arm = models.ForeignKey(StingDevice, null=True, blank=True, on_delete=models.SET_NULL,related_name = "stingsw")
    L1_sting_arm = models.ForeignKey(StingDevice, null=True, blank=True, on_delete=models.SET_NULL,related_name = "L1")
    L2_sting_arm = models.ForeignKey(StingDevice, null=True, blank=True, on_delete=models.SET_NULL,related_name = "L2")
    class Meta:
        verbose_name_plural= "sting settings"
        
class FileAttachments(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    run_sheet = models.FileField(null=True,blank=True)
    pretest_photo = models.ImageField(null=True,blank=True)
    posttest_photo= models.ImageField(null=True,blank=True)
    video = models.FileField(null=True,blank=True)

    class Meta:
        verbose_name_plural="file attachments"

class Condition(models.Model):
    name = models.CharField(max_length=100)
    current = models.FloatField(default=40,verbose_name="Current (A)")
    plasma_gas_flow = models.FloatField(default=0,verbose_name="plasma gas flow (g/s)")
    shield_gas_flow = models.FloatField(default=0,verbose_name="shield gas flow (g/s)")
    nozzle_diameter = models.FloatField(default=1,verbose_name="nozzle diameter (cm)")
    shield_gas = models.ForeignKey(Gas,null=True,on_delete=models.CASCADE, related_name = "Shield_gas")
    plasma_gas = models.ForeignKey(Gas,null=True,on_delete=models.CASCADE, related_name = "Plasma_gas")

    def __str__(self):
        return self.name

class ConditionInstance(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dwell_time = models.FloatField(default=200,verbose_name="dwell time (s)")
    start_time = models.FloatField(verbose_name="start time (s)",null=True,blank=True)
    end_time = models.FloatField(verbose_name="end time (s)",null=True,blank=True)

    def __str__(self):
        return self.name

class StingInsertion(models.Model):
    swivel_sting_duration = models.FloatField(default=0,verbose_name="swivel sting duration (s)")
    L1_sting_duration = models.FloatField(default=0,verbose_name="L1 sting duration (s)")
    L2_sting_duration = models.FloatField(default=0,verbose_name="L2 sting duration (s)")

    def __str__(self):
        return self.name
