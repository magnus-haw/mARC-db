from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from data.models import Diagnostic,Test,Run,Record,Apparatus,Series
from data.forms import SearchForm,UploadTestForm,UploadRunForm
from system.models import Condition, ConditionInstance,Cathode,HeaterSettings
from stats.models import ConditionAggregate

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column

from numpy import array,nanmin,nanmax,shape,where,nanmean,nanstd
import pandas as pd

# Create your views here.

def ConditionView(request,condition_pk):
    cd = Condition.objects.get(pk=condition_pk)
    insts = cd.conditioninstance_set.all()
    aggs = ConditionAggregate.objects.filter(instance__in=insts).order_by('diagnostic')
    
    context = {
            'condition':cd,
            'aggs':aggs,
            }
    return render(request, 'stats/condition_detail.html', context = context)


def getStats():
    cds = Condition.objects.all()
    for cd in cds:
        print('\n\n\n',cd.name)
        cdinstances = cd.conditioninstance_set.all()
        for inst in cdinstances:
            print(inst.run.name)
            df = inst.run.get_dataframe()
            time = df["Time [s]"].values
            inds = where((time >= inst.start_time) & (time < inst.end_time))[0]
            cnames = df.columns
            for i in range(1,len(cnames)):
                #print(time[inds],inds,inst.start_time,inst.end_time)
                myslice = df[cnames[i]][inds].dropna()
                #print(type(myslice),myslice)
                avg,stdev,mmin,mmax = myslice.mean(),myslice.std(),myslice.min(),myslice.max()
                diag = Diagnostic.objects.get(name=cnames[i],apparatus=inst.run.test.apparatus)
                print(avg,stdev,diag.name)
                agg,created_agg = ConditionAggregate.objects.get_or_create(instance=inst, diagnostic=diag)
                agg.avg = avg
                agg.stdev = stdev
                agg.min = mmin
                agg.max = mmax
                agg.save()
    return
            
def cathodeTime():
    ### calculate cathode time
    caths = Cathode.objects.all()
    for cath in caths:
        cathtime = 0
        hsets = cath.heatersettings_set.all()
        for hset in hsets:
            cathtime += hset.total_arc_on_duration
        cath.runtime = cathtime
        cath.save()
    return

def conditionCharac():
    cds = Condition.objects.all()
    alldata = pd.DataFrame()
    for cd in cds:
        insts = cd.conditioninstance_set.all()
        aggs = ConditionAggregate.objects.filter(instance__in=insts).order_by('diagnostic')
        diags = aggs.values_list('diagnostic__pk',flat=True).distinct()
        data = {}
        
        for diag in diags:
            dobj = Diagnostic.objects.get(pk=diag)
            vals = aggs.filter(diagnostic__pk= diag).values_list('avg',flat=True)
            avg = nanmean(vals)
            stdev = nanstd(vals)
            data[dobj.name] = [avg]
            data[dobj.name+'_stdev'] = [stdev]
        df = pd.DataFrame(data=data,index=[cd.name,])
        alldata= alldata.append(df,sort=False)
    return alldata
