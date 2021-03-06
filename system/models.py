from django.db import models
from data.models import Run, Diagnostic, Person, Apparatus
from units.models import ComboUnit

# Create your models here.
class Gas(models.Model):
    name = models.CharField(max_length=200,unique=True)
    abbrv = models.CharField(max_length=6,null=True,blank=True,unique=True)
    molecular_weight = models.FloatField(blank=True, null=True)
    ionization_energy = models.FloatField(blank=True, null=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "gases"

class Material(models.Model):
    name = models.CharField(max_length=200,unique=True)
    abbrv = models.CharField(max_length=6,null=True,blank=True,unique=True)
    description = models.TextField(blank=True, null=True)
    molecular_weight = models.FloatField(blank=True, null=True)
    ionization_energy = models.FloatField(blank=True, null=True)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class TestSample(models.Model):
    name = models.CharField(max_length=200,unique=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    shape = models.CharField(max_length=50)
    diameter = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    diagnostics = models.ManyToManyField(Diagnostic)
    notes = models.TextField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class StingDevice(models.Model):
    name = models.CharField(max_length=200)
    diagnostic = models.ForeignKey(Diagnostic,on_delete=models.SET_NULL, null=True, blank=True)
    #sample = models.ForeignKey(Coupon) ->TODO
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class StingArm(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

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
    name = models.CharField(max_length=200)
    diameter = models.FloatField(verbose_name="Diameter (cm)",null=True)
    installed = models.DateField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    photo = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

class Cathode(models.Model):
    name = models.CharField(max_length=200)
    TUNGSTEN = 'W'
    SILVERPLUS = 'Ag+'
    COPPER = 'Cu'
    CATHODETYPES = [
        (TUNGSTEN, 'Tungsten'),
        (SILVERPLUS, 'SilverPlus'),
        (COPPER, 'Copper'),
    ]
    type = models.CharField(
        max_length=3,
        choices=CATHODETYPES,
        default=SILVERPLUS,
    )
    installed = models.DateField(blank=True,null=True)
    removed = models.DateField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    preinstall_photo = models.ImageField(blank=True,null=True)
    postremoval_photo= models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.name

class Disk(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True,null=True)
    photo = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

class CameraSettings(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera,blank=True,null=True,on_delete=models.SET_NULL)
    lens   = models.ForeignKey(Lens,blank=True,null=True,on_delete=models.SET_NULL)
    opticalfilter = models.ForeignKey(OpticalFilter,blank=True,null=True,on_delete=models.SET_NULL)
    CameraPosition = models.ForeignKey(CameraPosition,blank=True,null=True,on_delete=models.SET_NULL)
    VIDEO = 'Video'
    STILL = 'Still'
    RECORDTYPES = [
        (VIDEO, 'Video'),
        (STILL, 'Still'),
    ]
    record_type = models.CharField(max_length=5,choices=RECORDTYPES,blank=True, null=True)

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
      
class SettingAttachment(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField()
    DOCUMENT = 'DOC'
    IMAGE = 'IMG'
    VIDEO = 'VID'
    DATA = 'DAT'
    OTHER = 'OTR'
    FILETYPES = [
        (DOCUMENT, 'Document'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (DATA, 'Data'),
        (OTHER, 'Other'),
    ]
    type = models.CharField(
        max_length=3,
        choices=FILETYPES,
        default=DOCUMENT,
    )
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural="file attachment"

class Condition(models.Model):
    name = models.CharField(max_length=100)
    current = models.FloatField(default=40,verbose_name="Current (A)")
    plasma_gas_flow = models.FloatField(default=0,verbose_name="plasma gas flow (g/s)")
    shield_gas_flow = models.FloatField(default=0,verbose_name="shield gas flow (g/s)")
    nozzle = models.ForeignKey(Nozzle,null=True,on_delete=models.SET_NULL, related_name = "Nozzle")
    disks = models.PositiveIntegerField(default=2)
    shield_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL, related_name = "Shield_gas")
    plasma_gas = models.ForeignKey(Gas,null=True,on_delete=models.SET_NULL, related_name = "Plasma_gas")
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_num_repr(self):
        listvalues = [self.current/100, self.plasma_gas_flow, self.shield_gas_flow, self.nozzle.diameter, 
                      self.disks, self.shield_gas.molecular_weight, self.plasma_gas.molecular_weight]
        
        return listvalues
    
    class Meta:
        ordering = ['name']
        
class ConditionInstance(models.Model):
    run = models.ForeignKey(Run,on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dwell_time = models.FloatField(default=60,verbose_name="dwell time (s)",null=True,blank=True)
    valid = models.BooleanField(null=True,blank=True)
    
    #Sting arm section
    sweep_insertion = models.FloatField(verbose_name="Sweep arm dwell time (s)",null=True,blank=True)
    sweep_devices = models.ManyToManyField(StingDevice, blank=True, related_name='sweep_devices')

    l1_insertion = models.FloatField(verbose_name="L1 arm dwell time (s)",null=True,blank=True)
    l1_devices = models.ManyToManyField(StingDevice, blank=True, related_name='l1_devices')

    l2_insertion = models.FloatField(verbose_name="L2 arm dwell time (s)",null=True,blank=True)
    l2_devices = models.ManyToManyField(StingDevice, blank=True, related_name='l2_devices')
    
    def __str__(self):
        return self.run.name+ "_" +self.name

    class Meta:
        ordering = ['run__date']

class Component(models.Model):
    name = models.CharField(max_length=200)
    critical = models.BooleanField(default=False)
    type = models.CharField(max_length=100)
    subsystem = models.ForeignKey('Subsystem', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True,null=True)
    installed = models.DateTimeField(blank=True,null=True)
    removed = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.name

class ComponentFile(models.Model):
    component = models.ForeignKey(Component,on_delete=models.CASCADE)
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
    description = models.TextField(blank=True,null=True)

class Subsystem(models.Model):
    apparatus = models.ForeignKey(Apparatus, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=25)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class SubsystemConfig(models.Model):
    name = models.CharField(max_length=200)
    subsystem = models.ForeignKey('Subsystem', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True,null=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.subsystem.name + str(self.date)

class SubsystemConfigItem(models.Model):
    config = models.ForeignKey('SubsystemConfig', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value1_name = models.FloatField(null=True, blank=True)
    value1 = models.FloatField(null=True, blank=True)
    value1_unit = models.ForeignKey(ComboUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name="val1unit")
    value2_name = models.FloatField(null=True, blank=True)
    value2 = models.FloatField(null=True, blank=True)
    value2_unit = models.ForeignKey(ComboUnit, on_delete=models.SET_NULL, null=True, blank=True, related_name="val2unit")
    
    description = models.TextField(blank=True,null=True)
    component = models.ForeignKey('Component', on_delete=models.SET_NULL, null=True, blank=True)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name
