
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mARC.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from system.models import *
from data.models import *

app = Apparatus.objects.filter(name__contains="2.0").first()

### arc column subsystem
column,added = Subsystem.objects.get_or_create(name = "Arc Column", description="mARC column components",
                                         type="column", apparatus=app)

nozzle = Nozzle.objects.first()
nozzle_component,added = Component.objects.get_or_create(name="Nozzle_0.735in", type="nozzle", description="copper nozzle, 0.735in exit diameter", critical=True, installed=nozzle.installed)
nozzle_component.save()

cathodes = Cathode.objects.all()
for cathode in cathodes:
    _component,added = Component.objects.get_or_create(name=cathode.name, type="cathode", description=cathode.description, critical=True, installed=cathode.installed, removed=cathode.removed)
    _component.save()

disks = Disk.objects.all()
for disk in disks:
    _component,added = Component.objects.get_or_create(name=disk.name, type="disk", description="basic constrictor disk", critical=True)
    _component.save()

### Cameras? -> diagnostics
lenses = Lens.objects.all()
for lense in lenses:
    _component,added = Component.objects.get_or_create(name=lense.name, type="lense", description=lense.name, critical=False)
    _component.save()

filters = OpticalFilter.objects.all()
for fil in filters:
    _component,added = Component.objects.get_or_create(name=fil.name, type="optical filter", description=fil.name, critical=False)
    _component.save()

