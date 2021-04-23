from django.db import transaction
from django.db.models import Avg, Min, Max
from django.shortcuts import render

from stats.models import ConditionInstanceFit, SeriesStableStats, SeriesStartupStats
from stats.models import RunUsage, DiagnosticConditionAverage, Flag
from system.models import Condition, ConditionInstance
from data.models import Run, Apparatus, Diagnostic

from stats.utils import infer_conditions, collate_conditions, get_condition_match
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

# Create your views here.

def updateAllStats(apparatus):
    conditionInstances = ConditionInstance.objects.exclude(valid=False)
    updateConditionInstanceFits(conditionInstances)

    conditionInstanceFits = ConditionInstanceFit.objects.exclude(instance__valid=False)
    updateSeriesStats(conditionInstanceFits)

    conditions = Condition.objects.all()
    updateConditionAvgs(apparatus,conditions)

    updateRunUsage(apparatus)

# @transaction.atomic
def updateConditionInstanceFits(conditionInstances, plot=False):
    """Update time-series fits for list of condition instances
    """
    ### Loop over all existing condition instances
    for ci in conditionInstances:
        print(ci)
        ### Search through data & determine if current & flow diags are present
        series = ci.run.diagnosticseries_set.all()
        dg_inputs = Diagnostic.objects.filter(apparatus=ci.run.test.apparatus, category='INPUT')
        currentlist = series.filter(diagnostic__name="Arc Current [A]")
        flowlist = series.filter(diagnostic__name="Plasma gas [g/s]")

        ### Only produce stats if current, massflow diagnostics are present
        if len(currentlist)==1 and len(flowlist)==1:
            current = currentlist[0]
            flow = flowlist[0]
            ti,I = current.time.time, current.values
            tf,F = flow.time.time, flow.values

            ### Segment data based on current and flow diagnostics
            condsI = infer_conditions(ti,I)
            condsF = infer_conditions(tf,F, minval=0.1, thresh=.05)
            condsall = collate_conditions(condsI,condsF)

            ### Loop over identified conditions & match to planned conditions
            for cond in condsall:
                if get_condition_match(cond,ci):
                    ### Plot
                    if plot:
                        plt.plot(tf,F)
                        plt.plot(ti,I/200.)
                        plt.plot([cond['stable_start'],cond['stable_start']], [0,.8], 'k-')
                        plt.plot([cond['stable_end'],cond['stable_end']], [0,.8], 'k-')
                        plt.show()

                    ### Save fit values from segmentation
                    if hasattr(ci, 'conditioninstancefit'):
                        cif = ci.conditioninstancefit
                        cif.instance= ci
                        cif.start= cond['start']
                        cif.end= cond['end']
                        cif.stable_start=cond['stable_start']
                        cif.stable_end=cond['stable_end']
                    else:
                        cif = ConditionInstanceFit(instance= ci, start= cond['start'], end= cond['end'],
                                            stable_start=cond['stable_start'],stable_end=cond['stable_end'])
                    cif.save()

def updateFlags(conditionInstances):
    """Update flags for condition instances
    """
    dg_inputs = Diagnostic.objects.filter(apparatus=ci.run.test.apparatus, category='INPUT')
    dg_flag_missing = Diagnostic.objects.filter(apparatus=ci.run.test.apparatus, flag_if_missing=True)
    ### Loop over all existing condition instances
    for ci in conditionInstances:
        ### Search through data & determine if all input diagnostics are present
        series = ci.run.diagnosticseries_set.all()
        run = ci.run
        for dg_in in dg_inputs:
            if not series.filter(id=dg_in.id).exists():
                Flag.objects.get_or_create(run=run, rating=1, description=dg_in.name+" missing")
        for dg_in in dg_flag_missing:
            if not series.filter(id=dg_in.id).exists():
                Flag.objects.get_or_create(run=run, rating=0, description=dg_in.name+" missing")
        

# @transaction.atomic
def updateSeriesStats(conditionInstanceFits):
    for cif in conditionInstanceFits:
        print(cif)
        ### Loop over diagnostics & create series stat objects
        dg_series = cif.instance.run.diagnosticseries_set.all()
        for dgs in dg_series:
            ts = dgs.time.time 
            vals = dgs.values

            # stable segment stats
            t0,t1 = cif.stable_start, cif.stable_end
            inds = (ts>t0)*(ts<t1)
            t,v = ts[inds],vals[inds]
            avg = np.nanmean(v)
            stdev = np.nanstd(v)
            vmin,vmax = np.nanmin(v),np.nanmax(v)
            
            sss = SeriesStableStats.objects.filter(condition=cif, series=dgs)
            if sss.exists():
                pass
                # sss.update(series=dgs, condition=cif,avg=avg,stdev=stdev,min=vmin,max=vmax)
            else:
                new_sss = SeriesStableStats(series=dgs, condition=cif,avg=avg,stdev=stdev,min=vmin,max=vmax)
                new_sss.save()

            # startup stats
            t0,t1 = cif.start, cif.stable_start
            inds = (ts>t0)*(ts<t1)
            t,v = ts[inds],vals[inds]
            stdev = np.nanstd(v)
            vmin,vmax = np.nanmin(v),np.nanmax(v)

            sss = SeriesStartupStats.objects.filter(condition=cif, series=dgs)
            if sss.exists():
                pass
                # sss.update(series=dgs,condition=cif,dt=t1-t0,stdev=stdev,min=vmin,max=vmax)
            else:
                new_sss = SeriesStartupStats(series=dgs,condition=cif,dt=t1-t0,stdev=stdev,
                                            min=vmin,max=vmax)
                new_sss.save()

# @transaction.atomic
def updateConditionAvgs(apparatus, conditions):
    ### select diagnostics from single apparatus
    dgs = Diagnostic.objects.filter(apparatus=apparatus)

    ### loop over conditions & diagnostics
    for condition in conditions:
        for dg in dgs:
            print(condition, dg)
            ### collect stats for given condition and diagnostic
            sss = SeriesStableStats.objects.filter(condition__instance__condition=condition, series__diagnostic = dg)
            if sss.exists():
                ### produce aggregate stats if data is present
                n = sss.count()
                s_avg = sss.aggregate(Avg('avg'))

                if n < 3:
                    s_min = sss.aggregate(Min('min'))
                    s_max = sss.aggregate(Max('max'))
                    s_err = (s_max['max__max']-s_min['min__min'])/2.
                else:
                    s_err = np.std(sss.values_list('avg', flat= True))

                dg_cond_avg = DiagnosticConditionAverage.objects.filter(condition=condition, diagnostic=dg)
                if dg_cond_avg.exists():
                    dg_cond_avg.update(value = s_avg['avg__avg'],err=s_err,
                                    npoints=n)
                else:
                    new_avg = DiagnosticConditionAverage(condition=condition, diagnostic=dg, value = s_avg['avg__avg'],
                                                         err=s_err, npoints=n)
                    new_avg.save()

def updateRunUsage(apparatus):
    """Updates usage statistics for each run (time on, power used, total gasflow mass)

    Args:
        apparatus ([type]): specific apparatus
    """
    ### select diagnostics from single apparatus
    runs = Run.objects.filter(test__apparatus =apparatus)

    ### loop over conditions & diagnostics
    for run in runs:
        ru = RunUsage.objects.filter(run=run)
        if ru.exists():
            pass
        else:
            # Extract various setting diagnostics
            series = run.diagnosticseries_set.all()
            currentlist = series.filter(diagnostic__name="Arc Current [A]")
            voltagelist = series.filter(diagnostic__name="Arc Voltage [V]")
            flowlist = series.filter(diagnostic__name="Plasma gas [g/s]")

            # search for existing condition instances
            instances = ConditionInstance.objects.filter(run=run)
            if len(instances) > 0:
                # Find global start and endtime for all instances in run
                times = []
                for ci in instances:
                    if hasattr(ci,'conditioninstancefit'):
                        cif = ci.conditioninstancefit
                        times.append(cif.end); times.append(cif.start)
                if len(times)==0:
                    # assume base settings for all quantities
                    I = ci.condition.current
                    f = ci.condition.plasma_gas_flow 
                    times=[0,ci.dwell_time + 30]
                    V = I*(-0.185) + 66.274*f + 89.03

                    totaltime = max(times) - min(times)
                    # calculate integral of power input
                    totalenergy = V*I*totaltime
                    # calculate integral of mass flow
                    totalmass = f*totaltime
                else:
                    totaltime = max(times) - min(times)
                    ti = np.linspace(min(times),max(times),1500)

                    #Extract or predict current
                    if len(currentlist)==0:
                        I = np.ones(len(ti))*ci.condition.current
                    else:
                        current = currentlist[0]
                        I = current.interp(ti)
                    
                    #Extract or predict mass flow
                    if len(flowlist)==0:
                        f = np.ones(len(ti))*ci.condition.plasma_gas_flow 
                    else:
                        flow = flowlist[0]
                        f = flow.interp(ti)
                    
                    #Extract or predict voltage
                    if len(voltagelist)==0:
                        V = I*(-0.185) + 66.274*f + 89.03
                    else:
                        voltage = voltagelist[0]
                        V = voltage.interp(ti)
                    
                    # calculate integral of power input
                    totalenergy = np.trapz(V*I,x=ti)
                    # calculate integral of mass flow
                    totalmass = np.trapz(f,x=ti)

                new_ru = RunUsage(run=run,time=totaltime,energy=totalenergy, mass = totalmass, notes="")
                new_ru.save()
                print(run.test, run, totaltime, totalenergy, totalmass)