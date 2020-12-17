from django.db.models import Avg, Min, Max
from django.shortcuts import render
from system.models import Condition, ConditionInstance
from stats.models import ConditionInstanceFit, SeriesStableStats, SeriesStartupStats, DiagnosticConditionAverage
from data.models import Run, Apparatus, Diagnostic

from stats.utils import infer_conditions, collate_conditions, get_condition_match
import matplotlib.pyplot as plt
import numpy as np

# Create your views here.

def updateAllStats(apparatus):
    conditionInstances = ConditionInstance.objects.all()
    updateConditionInstanceFits(conditionInstances)

    conditionInstanceFits = ConditionInstanceFit.objects.all()
    updateSeriesStats(conditionInstanceFits)

    conditions = Condition.objects.all()
    updateConditionAvgs(apparatus,conditions)

def updateConditionInstanceFits(conditionInstances, plot=False):
    """Update statistics objects for all runs from given apparatus
    """
    ### Loop over all existing condition instances

    for ci in conditionInstances:
        ### Search through data & determine if current & flow diags are present
        series = ci.run.diagnosticseries_set.all()
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

def updateSeriesStats(conditionInstanceFits):
    for cif in conditionInstanceFits:
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
                sss.update(series=dgs, condition=cif,avg=avg,stdev=stdev,min=vmin,max=vmax)
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
                sss.update(series=dgs,condition=cif,dt=t1-t0,stdev=stdev,min=vmin,max=vmax)
            else:
                new_sss = SeriesStartupStats(series=dgs,condition=cif,dt=t1-t0,stdev=stdev,
                                            min=vmin,max=vmax)
                new_sss.save()

def updateConditionAvgs(apparatus, conditions):
    ### select diagnostics from single apparatus
    dgs = Diagnostic.objects.filter(apparatus=apparatus)

    ### loop over conditions & diagnostics
    for condition in conditions:
        for dg in dgs:
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
                    s_err = np.std(sss.values_list('avg'))

                dg_cond_avg = DiagnosticConditionAverage.objects.filter(condition=condition, diagnostic=dg)
                if dg_cond_avg.exists():
                    dg_cond_avg.update(value = s_avg['avg__avg'],err=s_err,
                                    npoints=n)
                else:
                    new_avg = DiagnosticConditionAverage(condition=condition, diagnostic=dg, value = s_avg['avg__avg'],
                                                         err=s_err, npoints=n)
                    new_avg.save()


