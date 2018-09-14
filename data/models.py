from django.db import models

# Create your models here.

class Spreadsheet(models.Model):
    filename = models.CharField(max_length=200,primary_key=True)
    date = models.DateField()
    notes = models.TextField(null=True)

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['date']

class Sheet(models.Model):
    name = models.CharField(max_length=200)
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
    columnBooleans = models.CharField(max_length=50)
    notes = models.TextField(null=True)
    cnames = ['Time [s]','Arc Voltage [V]','Current [A]',
        'ChamberPressure [Pa]','ColumnPressure [Pa]',
        'PlasmaGas [g/s]','ShieldGas [g/s]','AnodeDeltaT [degC]',
        'Cathode Return [degC]','Cathode Supply [degC]','CurrentSC [A]',
        'PitotTemp [degC]','PitotPressure [Pa]','GardonHeatFlux [W/cm^2]',
        'GardonTemp [degC]','PitotPosition [in]','GardonPosition [in]',
        'Vacuumpumps [Pa]','String Pot Vex [in]','KurtLeskerPirani [Pa]',
        'B-RAX-Pirani [V]']
    class Meta:
        unique_together = (("name", "spreadsheet"),)
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def list_diagnostics(self):
        myd,mypk = [],[]
        for c in range(0,len(self.columnBooleans)):
            if self.columnBooleans[c] == '1':
                myd.append(self.cnames[c])
                mypk.append(c+1)
        return zip(myd,mypk)

class Diagnostic(models.Model):
    name = models.CharField(max_length=50,unique=True)
    units = models.CharField(max_length=50)
    notes = models.TextField(blank=True,null=True)
    sensor= models.CharField(max_length=200)
    description = models.TextField()
    resolution = models.FloatField(blank=True,null=True)
    noise = models.FloatField(blank=True,null=True)
    key = models.CharField(max_length=50,unique=True,blank=True,null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']

class Record(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    time    = models.FloatField(verbose_name='Time [s]')
    voltage = models.FloatField(null=True,blank=True,verbose_name='Arc Voltage [V]')
    current = models.FloatField(null=True,blank=True,verbose_name='Current [A]')
    chamber_pressure = models.FloatField(null=True,blank=True,verbose_name='ChamberPressure [Pa]')
    column_pressure  = models.FloatField(null=True,blank=True,verbose_name='ColumnPressure [Pa]')
    plasma_gas = models.FloatField(null=True,blank=True,verbose_name='PlasmaGas [g/s]')
    shield_gas = models.FloatField(null=True,blank=True,verbose_name='ShieldGas [g/s]')
    anode_deltaT = models.FloatField(null=True,blank=True,verbose_name='AnodeDeltaT [degC]')
    cathode_return = models.FloatField(null=True,blank=True,verbose_name='Cathode Return [degC]')
    cathode_supply =  models.FloatField(null=True,blank=True,verbose_name='Cathode Supply [degC]')
    currentSC =  models.FloatField(null=True,blank=True,verbose_name='CurrentSC [A]')
    pitot_temp =  models.FloatField(null=True,blank=True,verbose_name='PitotTemp [degC]')
    pitot_pressure =  models.FloatField(null=True,blank=True,verbose_name='PitotPressure [Pa]')
    gardon_heat_flux =  models.FloatField(null=True,blank=True,verbose_name='GardonHeatFlux [W/cm^2]')
    gardon_temp =  models.FloatField(null=True,blank=True,verbose_name='GardonTemp [degC]')
    pitot_position =  models.FloatField(null=True,blank=True,verbose_name='PitotPosition [in]')
    gardon_position =  models.FloatField(null=True,blank=True,verbose_name='GardonPosition [in]')
    vacuumpump_pressure =  models.FloatField(null=True,blank=True,verbose_name='Vacuumpumps [Pa]')
    vex_position =  models.FloatField(null=True,blank=True,verbose_name='String Pot Vex [in]')
    kurtlesker_pirani =  models.FloatField(null=True,blank=True,verbose_name='KurtLeskerPirani [Pa]')
    B_RAX_pirani =  models.FloatField(null=True,blank=True,verbose_name='B-RAX-Pirani [V]')
    mask_data = models.BooleanField(default=False)
    flags = models.CharField(max_length=50)

    class Meta:
        unique_together = (("sheet", "spreadsheet","time"),)
        ordering = ['time']

