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

class CameraPosition(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class OpticalFilter(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class Lens(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="lenses"

class Camera(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class Nozzle(models.Model):
    name = models.CharField(max_length=100)
    diameter = models.FloatField(verbose_name="Diameter (inch)",null=True)
    notes = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class StingArm(models.Model):
    name = models.CharField(max_length=15)
    notes = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name

class CalShape(models.Model):
    name = models.CharField(max_length=15)
    notes = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name

class CalType(models.Model):
    name = models.CharField(max_length=15)
    notes = models.TextField(null=True,blank=True)
   
    def __str__(self):
        return self.name

class CameraSettings(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera,blank=True,null=True,on_delete=models.SET_NULL)
    lens   = models.ForeignKey(Lens,blank=True,null=True,on_delete=models.SET_NULL)
    opticalfilter = models.ForeignKey(OpticalFilter,blank=True,null=True,on_delete=models.SET_NULL)
    CameraPosition = models.ForeignKey(CameraPosition,blank=True,null=True,on_delete=models.SET_NULL)

class VacuumWaterLoop(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    ex_pressure = models.FloatField(verbose_name="VPW-PI-220 heat ex. Press (PSIG)",null=True)
    ex_flow= models.FloatField(verbose_name="VPW-FI-220 heat ex. Press (GPM)",null=True)
    vac_pressure = models.FloatField(verbose_name="VPW-PI-230 vac. pump Press. (PSIG)",null=True)
    vac_flow = models.FloatField(verbose_name="VPW-FI-230 vac. pump Flow (GPM)",null=True)
    vac_exit_temperature = models.FloatField(verbose_name="VPW-TI-280 vac. pump exit T (F)",null=True)
    
class SensorWaterLoop(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    temperature = models.FloatField(verbose_name="SKW-TI-401 Temp (F)",null=True)
    conductivity= models.FloatField(verbose_name="SKW-ST-401 Conduct. (uS)",null=True)
    arc_supply_pressure = models.FloatField(verbose_name="SKW-PI-440 sensor supply (PSIG)",null=True)
    
class DistilledWaterLoop(models.Model):
    run = models.OneToOneField(Run,on_delete=models.CASCADE,primary_key=True)
    temperature = models.FloatField(verbose_name="HCW-TI-101 Temp (F)",null=True)
    conductivity= models.FloatField(verbose_name="HCW-ST-101 Conduct. (uS)",null=True)
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
    nozzle = models.ForeignKey(Nozzle,null=True,on_delete=models.SET_NULL)
    total_cathode_time = models.FloatField(null=True,verbose_name="total cathode time (s)")
    total_arc_on_duration = models.FloatField(null=True,verbose_name="total arc-on duration (s)")
    number_disks = models.PositiveSmallIntegerField(null=True,default=2)
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
    spectra = models.FileField(null=True,blank=True)

    class Meta:
        verbose_name_plural="file attachments"

class PhotoAttachment(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    photo = models.ImageField(null=True,blank=True)

    class Meta:
        verbose_name_plural="photos"

##class FileAttachment(models.Model):
##    run = models.ForeignKey(Run,on_delete=models.CASCADE)
##    file = models.FileField(null=True,blank=True)
##
##    class Meta:
##        verbose_name_plural="files"

class Condition(models.Model):
    name = models.CharField(max_length=100)
    current = models.FloatField(default=40,verbose_name="Current (A)")
    plasma_gas_flow = models.FloatField(default=0,verbose_name="plasma gas flow (g/s)")
    shield_gas_flow = models.FloatField(default=0,verbose_name="shield gas flow (g/s)")
    nozzle = models.ForeignKey(Nozzle,null=True,on_delete=models.SET_NULL, related_name = "Nozzle")
    shield_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL, related_name = "Shield_gas")
    plasma_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL, related_name = "Plasma_gas")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
class ConditionInstance(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_time = models.FloatField(verbose_name="start time (s)",null=True)
    end_time = models.FloatField(verbose_name="end time (s)",null=True)
    dwell_time = models.FloatField(default=60,verbose_name="dwell time (s)",null=True,blank=True)

    def __str__(self):
        return self.name

class StingInsertion(models.Model):
    swivel_sting_duration = models.FloatField(default=0,verbose_name="swivel sting duration (s)")
    L1_sting_duration = models.FloatField(default=0,verbose_name="L1 sting duration (s)")
    L2_sting_duration = models.FloatField(default=0,verbose_name="L2 sting duration (s)")

    def __str__(self):
        return self.name
