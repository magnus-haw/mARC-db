from .models import Disk, Cathode
from data.models import Run
from system.models import ConditionInstance, Condition

def getCathodeTime(mycathode):
    runs = mycathode.run_set.all()
    cinstances = ConditionInstance.objects.filter(run__in=runs)
    dt=0
    for cinst in cinstances:
        if hasattr(cinst, 'conditioninstancefit')
            dt += cinst.conditioninstancefit.end - cinst.conditioninstancefit.start


def getDiskTime(mydisk):
    pass

def getCathodeUsedPower():
    pass

def getDiskUsedPower():
    pass

def getCathodeRuns():
    pass

