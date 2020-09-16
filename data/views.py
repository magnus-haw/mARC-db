from data.models import Diagnostic,Test,Run,Record,Apparatus,Series
from data.forms import SearchForm,UploadTestForm,UploadRunForm

from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column

from numpy import array,nanmin,nanmax,shape
import pandas as pd
import csv
import time

def index(request):
    num_apparatus = Apparatus.objects.count()
    num_tests = Test.objects.count()
    num_runs = Run.objects.count()
    context = {
        'num_apparatus':num_apparatus,
        'num_tests':num_tests,
        'num_runs':num_runs,
            }
    return render(request, 'index.html', context=context)

def ApparatusListView(request):
    apps = Apparatus.objects.all()
    
    context = {
        'apparatus':apps,
            }
    return render(request, 'data/apparatus_list.html', context=context)

def ApparatusDetailView(request,apparatus_pk):
    app = get_object_or_404(Apparatus, pk=apparatus_pk)
    test_set = app.test_set.all()
    
    context = {
            'apparatus':app,
            'tests':test_set,
            }
    return render(request, 'data/apparatus_detail.html', context = context)

def TestView(request,test_pk):
    test = Test.objects.get(pk=test_pk)
    
    context = {
            'test':test,
            'apparatus':test.apparatus,
            }
    return render(request, 'data/test_detail.html', context = context)

def find_diagnostic(name,apparatus):
    dgs = Diagnostic.objects.filter(name = name, apparatus=apparatus)
    if len(dgs)==1:
        return dgs[0]
    else:
        dgs = Diagnostic.objects.filter(apparatus=apparatus)
        for dg in dgs:
            if name in dg.alternatediagnosticname_set.values_list('name',flat=True):
                return dg
        return None

def upload_run(runname,df,test,batch_size=100):
    print(df.describe(),test,runname)
    if df.columns[0] != '':
        run,created_run = Run.objects.get_or_create(name=runname, test=test)
        run.save()
        
        for col_name in df.columns:            
            diagnostic = find_diagnostic(col_name,test.apparatus.pk)
            if diagnostic != None:
                series,created_series = Series.objects.get_or_create(name=runname+"_"+diagnostic.name,
                                                                     run=run,diagnostic=diagnostic)
                if created_series:
                    print(series.diagnostic)
                    series.save()
                
                    cdata = df[col_name].values
                    objs = [Record(series=series,index=i,value=cdata[i]) for i in range(0,len(cdata))]
                    Record.objects.bulk_create(objs,batch_size)    
    return

@transaction.atomic
def upload_csv(request,test_pk):
    ### After file is chosen and uploaded, do this
    if request.method == 'POST':
        form = UploadRunForm(request.POST, request.FILES)
        success = False
        if form.is_valid():
            csv_file = request.FILES["file"]
            run_name = form.cleaned_data['name']
        
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return render(request, "data/upload_csv.html",
                              context={"test_pk":test_pk,
                                       "success":success,
                                       "show_response":True,
                                       "form":form,
                                      })
            try:
                test = Test.objects.get(pk=test_pk)
                df = pd.read_csv(csv_file)
                upload_run(run_name,df,test)
                success=True
                
            except Exception as e:
                #logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
                messages.error(request,"Unable to upload file. "+repr(e))

        ### After upload redirect to here
        return render(request, "data/upload_csv.html",
                      context={
                          "test_pk":test_pk,
                          "success":success,
                          "show_response":True,
                          "form":form,
                          })
    else: # Show upload form
        form = UploadRunForm()
        return render(request, "data/upload_csv.html",
                      context={
                          "test_pk":test_pk,
                          "show_response":False,
                          "form":form,
                          })

@transaction.atomic
def upload_xlsx(request,apparatus_pk):
    ### After file is chosen and uploaded, do this
    if request.method == 'POST':
        form = UploadTestForm(request.POST, request.FILES)
        success = False
        if form.is_valid():
            file = request.FILES["file"]
            date = form.cleaned_data['date']
            test_name = form.cleaned_data['name']

            if not file.name.endswith('.xlsx'):
                messages.error(request,'File is not xlsx type')
                return render(request, "data/upload_xlsx.html",
                              context={"apparatus_pk":apparatus_pk,
                                       "success":success,
                                       "show_response":True,
                                       "form":form,
                                      })
            try:
                dfdict = pd.read_excel(file,sheet_name=None)

                app = Apparatus.objects.get(pk=apparatus_pk)
                test,test_created = Test.objects.get_or_create(name=test_name,apparatus=app,date=date)
                
                for sheetname,df in dfdict.items():
                    upload_run(sheetname,df,test)
                success=True
                
            except Exception as e:
                #logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
                messages.error(request,"Unable to upload file. "+repr(e))

        ### After upload redirect to here
        return render(request, "data/upload_xlsx.html",
                      context={
                          "apparatus_pk":apparatus_pk,
                          "success":success,
                          "show_response":True,
                          "form":form,
                          })
    else: # Show upload form
        form = UploadTestForm()
        return render(request, "data/upload_xlsx.html",
                      context={
                          "apparatus_pk":apparatus_pk,
                          "show_response":False,
                          "form":form,
                          })
    

def ViewDiagnostic(request,pk):
    dg = get_object_or_404(Diagnostic, pk=pk)

    series_set = Series.objects.filter(diagnostic=pk)
    run_list = list(set(series_set.values_list('run',flat=True)))
    run_set = Run.objects.filter(name__in=run_list)
    test_list = list(set(run_set.values_list('test',flat=True)))
    test_set = Test.objects.filter(name__in=test_list)
    
    context = {
            'diagnostic':dg,
            'runs':run_set,
            'test_list':test_set,
            }
    return render(request, 'data/diagnostic_detail.html', context = context)

def DownloadRunCSV(request,run_pk):
    run = get_object_or_404(Run, pk=run_pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"'%(run.test.name+'_'+run.name+'_'+'mARC.csv')
    writer = csv.writer(response)

    df = run.get_dataframe()
    writer.writerow(df.columns)
    writer.writerows(df.values)
    return response

def SearchView(request):
    apps = Apparatus.objects.all()
    
    context = {
        'apparatus':apps,
            }
    return render(request, 'search-base.html', context=context)

def SearchData(request,apparatus_pk):
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            tests = form.cleaned_data['tests']
            diags =  form.cleaned_data['diagnostics']
            tname = 'Time [s]'
            #time_diag = Diagnostic.objects.filter(name=tname)
            diags = diags 

            dflist,serieslist = [],[]
            for test in tests:
                runs = test.run_set.all()
                for r in runs:
                    series = r.series_set.filter(diagnostic__in=diags)
                    df = pd.DataFrame()
                    df.test = test.name
                    df.run = r.name
                    slist =[]
                    for s in series:
                        df[s.diagnostic.name] = s.record_set.all().order_by('index').values_list('value',flat=True)
                        slist.append(s.pk)
                    if len(series)>0:
                        ts = r.series_set.get(diagnostic__name = tname)
                        df[tname] = ts.record_set.all().order_by('index').values_list('value',flat=True)
                        serieslist += [ts.pk]+ slist
                        dflist.append(df)
            print(df.columns)
            
            mycolor_ind =0
            myfigs = []
            for d in diags.exclude(name=tname):
                fig = figure(x_axis_label= tname,y_axis_label=d.name,
                        plot_width =1000,plot_height =600)
                for df in dflist:
                    if d.name in df.columns:
                        fig.line(df[tname], df[d.name],line_width = 1, legend= df.run+'_'+df.test, line_color=mycolors[mycolor_ind])
                        mycolor_ind = (mycolor_ind+1)%len(mycolors)
                fig.legend.click_policy="hide"
                myfigs.append(fig)
            bigplot = column(*myfigs)
            try:
                script, div = components(bigplot)
            except:
                print('Plotting error')
                script,div = '','' 
            context = {'form': form,'serieslist':serieslist,'apparatus_pk':apparatus_pk,
                       'tests':tests,'diagnostics':diags,'script':script,'div':div}
            
            # render results:
            return render(request, 'search_results.html', context)
    
    else:
        form = SearchForm()
        form.fields["tests"].queryset = Test.objects.filter(apparatus__pk=apparatus_pk)
        form.fields['tests'].widget.attrs['size']='15'
        form.fields["diagnostics"].queryset = Diagnostic.objects.filter(apparatus__pk=apparatus_pk).exclude(name="Time [s]")
        form.fields['diagnostics'].widget.attrs['size']='15'

    context = {
        'form': form,
    }

    return render(request, 'search.html', context)

def DownloadSearchCSV(request,apparatus_pk):
    list_pks = request.GET.getlist('series')
    series = Series.objects.filter(pk__in=list_pks)

    dflist =[]
    for s in series:
        df = pd.DataFrame()
        label = s.diagnostic.name +'_'+ s.run.name + '_' + s.run.test.name
        df[label] = s.record_set.all().order_by('index').values_list('value',flat=True)
        dflist.append(df)
    df_all = pd.concat(dflist,axis=1)
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"'%('mARC_db_search_results.csv')
    writer = csv.writer(response)

    writer.writerow(df_all.columns)
    print(shape(df_all.values))
    writer.writerows(df_all.values)

    return response


def ViewRun(request,run_pk):
    run = get_object_or_404(Run, pk=run_pk)
    df = run.get_dataframe()
    diagnostics = run.get_diagnostics()
    
    ### Plotting section
    figs=[]
    xkey = "Time [s]"
    time = df[xkey].values
    cnames = df.columns
    for i in range(0,len(cnames)):
        if cnames[i] != xkey:
            p1 = figure(x_axis_label=xkey, y_axis_label=cnames[i],
                plot_width =1000,plot_height =300)
            p1.line(df[xkey], df[cnames[i]], legend= cnames[i], 
                line_width = 2, line_color=mycolors[i])
            p1.legend.click_policy="hide"
            figs.append(p1)

    #Store components 
    bigplot = column(*figs)
    script, div = components(bigplot)
    #except:
    #    print('Run plotting error')
    #    script,div = '',''
    return render(request, 'data/run_detail.html', {'run':run,'data':df,'script':script,'div':div,'diagnostics':diagnostics,})


mycolors = ['green','red','blue','cyan','orange','black','magenta','purple','olive','lime','yellow','gold','darkred','salmon','deeppink','coral','turquoise','teal','darkkhaki','khaki','navy','steelblue']
