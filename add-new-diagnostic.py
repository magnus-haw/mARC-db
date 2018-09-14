# Query the database/compare to excel
import pandas as pd
from numpy import shape, array, arange,zeros,ones,nan
from os import listdir
from os.path import isfile, join
from data.models import *
import datetime

##time = cnames[0]
##d = Diagnostic(name = time, units='[s]', sensor='Analog-to-Digital Acquisition (NI-cDAQ)', description = 'Several safety features are included in the design of the data acquisition system, protecting sensors, data modules, and operator: most sensor measurements are fed through a patch panel which in turn connects to the data acquisition system. Because of the high frequency/high voltage EMF characteristic to the Max200 power supply, the data system needs to be disconnected from the sensors during plasma striking. The patch panel allows simultaneous connection of all sensor data to the DAQ once the arc is established. To further prevent current spikes during operation to reach the data acquisition modules, an electrical isolator was installed between those sensors that are in contact with the plasma or the vacuum chamber potential and the DAQ. In addition, the DAQ is powered through an isolation transformer, removing the direct connection to ground. The NI-cDAQ includes three analog and one isothermal thermocouple input modules. The 24VDC power supply energizes the column pressure transducer, plasma mass flow meter, and signal isolator rack, whereas the 10VDC power supply feeds the position and stagnation pressure transducers. The NI-cDAQ chassis ground is attached to the ground terminal on the 24VDC power supply. The DAQ modules typically have a measurable range of either ±10VDC (analog module) or ±100mVDC (thermocouple module).', resolution =0.01)
##d.save()


##nm = cnames[1]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Ohio Semitronics Inc. (Model: VT7-007E-11-TP)',
##               description = 'Voltage between anode and cathode')
##d.save()


##nm = cnames[2]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Ohio Semitronics Inc. (Models: CTL-401/300 and CTA212HY42)',
##               description = 'Arc current')

##nm = cnames[3]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Kurt J. Lesker (Series 345)',
##               description = 'Chamber pressure measured on top of the vacuum chamber')

##nm = cnames[4]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Setra (Model: 720110CTA4T2CD9K)',
##               description = 'Column pressure measured in the second spacer disk')

##nm = cnames[5]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Sage Metering Inc (Model: SIP-030-DC24-AIR)',
##               description = 'Plasma gas flow')

##nm = cnames[6]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='?',
##               description = 'Shield gas flow')

##nm = cnames[7]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Delta-T Co. (Model 37)',
##               description = 'Temperature difference between supply and return in cooling water to anode')

##nm = cnames[8]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Type-T thermocouple',
##               description = 'Cathode cooling water return temperature')

##nm = cnames[9]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Type-T thermocouple',
##               description = 'Cathode cooling water supply temperature')

##nm = cnames[10]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='?',
##               description = '?')

##nm = cnames[11]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='thermocouple',
##               description = 'placed on the body of the pressure transducer at the inlet')

##nm = cnames[12]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Medtherm pitot probe Model 12-PP-6-10-50553',
##               description = 'The hemispherical water-cooled probe head is 4.75 mm in diameter and the pressure port is 0.81 mm in diameter. A temperature compensated piezoresistive pressure transducer (Endevco, model number 8530C-15) is used in combination with the probe head. In order to allow for fast reaction time (making it possible to obtain radial pressure profiles across the stream), the transducer was placed as close as possible to the probe head without needing separate cooling and it was electrically isolated from the probe via non-conductive tubing. The 1.59 mm diameter pressure line is connected to the transducer at a distance of approximately 16 cm away from the top of the pitot probe. In order to ensure that the temperature of the transducer does not exceed 90 degC as per specification, a thermocouple was placed on the body of the transducer at the inlet.')

##nm = cnames[13]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='Medtherm Gardon Gauge Model 12-3000',
##               description = 'Heat flux measured on Gardon gauge')

##nm = cnames[14]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='thermocouple',
##               description = 'Gardon gauge temperature')
##d.save()
##
##nm = cnames[15]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='UniMeasure (Model: LX-PA-10-NIN-NPC)',
##               description = 'Pitot sensor position: String potentiometers are attached to the handles of the push-pull manipulators to track the radial position of the sensors/models. The sting arm assemblies are not precision devices and have considerable amounts of play in roll-angle of their axis. Thissource of positional error is estimated to affect the probe head position by ~1mm.')
##d.save()
##
##
##nm = cnames[16]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='UniMeasure (Model: LX-PA-10-NIN-NPC)',
##               description = 'Gardon sensor position: String potentiometers are attached to the handles of the push-pull manipulators to track the radial position of the sensors/models. The sting arm assemblies are not precision devices and have considerable amounts of play in roll-angle of their axis. Thissource of positional error is estimated to affect the probe head position by ~1mm.')
##d.save()
##
##
##nm = cnames[17]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='?',
##               description = '?')
##d.save()
##
##
##nm = cnames[18]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='?',
##               description = '?')
##d.save()
##
##
##nm = cnames[19]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='?',
##               description = '?')
##d.save()
##
##
##nm = cnames[20]
##units = nm.split(' ')[-1]
##d = Diagnostic(name = nm, units=units, sensor='?',
##               description = '?')
##d.save()

