from django.shortcuts import render,render_to_response,get_object_or_404
from data.models import Diagnostic,Spreadsheet,Sheet,Record
from data.forms import SearchForm

from django.http import HttpResponse
from django.views import generic
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column

from numpy import array,nanmin,nanmax,shape
import pandas as pd
import csv

def index(request):
    num_spreadsheets = Spreadsheet.objects.count()
    num_sheets = Sheet.objects.count()
    num_records = Record.objects.count()
    context = {
            'num_spreadsheets':num_spreadsheets,
            'num_sheets':num_sheets,
            'num_records':num_records,
            }
    return render(request, 'index.html', context=context)

def SearchData(request):
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            sp = form.cleaned_data['spreadsheets']
            diag =  form.cleaned_data['diagnostics']
            
            inds,keys =[],[]
            for d in diag:
                inds.append(d.pk - 1)
                keys.append(d.key)

            mystr = r"^"
            for i in range(0,21):
                if i in inds:
                    mystr += '1'
                else:
                    mystr += '.'
            mystr += "$"
            
            dflist = []
            for ss in sp:
                shls = Sheet.objects.filter(spreadsheet=ss,columnBooleans__iregex=mystr)
                if len(shls) == 0:
                    sp = sp.exclude(pk=ss.pk)
                for sh in shls:
                    df = pd.DataFrame(list(sh.record_set.all().values('time',*keys).order_by('time')) )
                    df.spreadsheet = sh.spreadsheet.filename.rstrip('.xlsx')
                    df.sheet = sh.name
                    dflist.append(df)
            mycolor_ind =0
            myfigs = []
            for d in diag:
                fig = figure(x_axis_label= "Time [s]",y_axis_label=d.name,
                        plot_width =1000,plot_height =500)
                for df in dflist:
                    fig.line(df['time'], df[d.key],line_width = 1, legend= df.sheet+'_'+df.spreadsheet, line_color=mycolors[mycolor_ind])
                    mycolor_ind = (mycolor_ind+1)%len(mycolors)
                fig.legend.click_policy="hide"
                myfigs.append(fig)
            bigplot = column(*myfigs)
            try:
                script, div = components(bigplot)
            except:
                print('Sheet plotting error')
                script,div = '','' 
            context = {'form': form,'spreadsheets':sp,'diagnostics':diag,'script':script,'div':div}
            
            # render results:
            return render(request, 'search_results.html', context)
    
    else:
        form = SearchForm()

    context = {
        'form': form,
    }

    return render(request, 'search.html', context)

class SpreadsheetListView(generic.ListView):
    model = Spreadsheet

class SpreadsheetDetailView(generic.DetailView):
    model = Spreadsheet

class DiagnosticListView(generic.ListView):
    model = Diagnostic

def ViewDiagnostic(request,pk):
    dg = get_object_or_404(Diagnostic, pk=pk)
    ind = pk-1
    mystr = r"^"+ ind*"." + "1" + ".*$" 

    shls = Sheet.objects.filter(columnBooleans__iregex=mystr)
    spshls = shls.values_list('spreadsheet',flat=True)
    spshls = list(set(spshls))
    context = {
            'diagnostic':dg,
            'sheet_list':shls,
            'spreadsheet_list':spshls,
            }
    return render(request, 'data/diagnostic_detail.html', context = context)

def DownloadSheetCSV(request,pk):
    sh = get_object_or_404(Sheet, pk=pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"'%(sh.name+'_'+sh.spreadsheet.filename.rstrip('.xlsx')+'_'+'mARC.csv')
    writer = csv.writer(response)

    df = pd.DataFrame(list(sh.record_set.all().values().order_by('time')) )
    writer.writerow(df.columns)
    print(shape(df.values))
    writer.writerows(df.values)

    return response

def DownloadSearchCSV(request):
    dgs = request.GET.getlist('diagnostic')
    print(dgs)
    sps = request.GET.getlist('spreadsheet')
    print(sps)
    #sps,dgs = spsh_str.split(','), diag_str.split(',')
    sp = Spreadsheet.objects.filter(filename__in = sps)
    diag = Diagnostic.objects.filter(pk__in = dgs) 

    inds,keys =[],[]
    for d in diag:
        inds.append(d.pk - 1)
        keys.append(d.key)

    mystr = r"^"
    for i in range(0,21):
        if i in inds:
            mystr += '1'
        else:
            mystr += '.'
    mystr += "$"

    dflist = []
    for ss in sp:
        shls = Sheet.objects.filter(spreadsheet=ss,columnBooleans__iregex=mystr)
        if len(shls) == 0:
            sp = sp.exclude(pk=ss.pk)
        for sh in shls:
            df = pd.DataFrame(list(sh.record_set.all().values('time',*keys).order_by('time')) )
            df.rename(columns=lambda x: x+'_'+ss.filename+'_'+sh.name,inplace=True)
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


def ViewSheet(request,pk):
    sh = get_object_or_404(Sheet, pk=pk)
    ld = Sheet.objects.get(pk=pk).list_diagnostics()
    df = pd.DataFrame(list(sh.record_set.all().values().order_by('time')) )
    
    ### Plotting section
    xkeys = ['time','time','time','time','time','time','pitot_position','gardon_position']
    ykeys = ['voltage','current','column_pressure','chamber_pressure',
            'plasma_gas','shield_gas','pitot_pressure','gardon_heat_flux']

    figs=[]
    cb = sh.columnBooleans

    for i in range(0,len(xkeys),2):
        if (cb[colDict[ykeys[i]]-1]=='1') and (cb[colDict[ykeys[i+1]]-1]=='1'):
            p1 = figure(x_axis_label= labelDict[xkeys[i]],y_axis_label=labelDict[ykeys[i]],y_range=(0,df[ykeys[i]].max()),
                plot_width =1000,plot_height =300)
            p1.line(df[xkeys[i]], df[ykeys[i]], legend= labelDict[ykeys[i]], 
                line_width = 2, line_color=mycolors[i])
            
            p1.extra_y_ranges = {ykeys[i+1]: Range1d(start=0, end=df[ykeys[i+1]].max())}
            p1.add_layout(LinearAxis(y_range_name=ykeys[i+1], axis_label=labelDict[ykeys[i+1]]), 'right')
            p1.line(df[xkeys[i+1]], df[ykeys[i+1]], legend= labelDict[ykeys[i+1]], 
                line_width = 2, y_range_name=ykeys[i+1], color=mycolors[i+1])

            p1.legend.click_policy="hide"
            figs.append(p1)
        elif (cb[colDict[ykeys[i]]-1]=='1') or (cb[colDict[ykeys[i+1]]-1]=='1'):
            if cb[colDict[ykeys[i]]-1]=='1':
                ykey = ykeys[i]
                xkey = xkeys[i]
            else:
                ykey = ykeys[i+1]
                xkey = xkeys[i+1]
            
            p1 = figure(x_axis_label= labelDict[xkey],y_axis_label=labelDict[ykey],y_range=(0,df[ykey].max()),
                plot_width =1000,plot_height =300)
            p1.line(df[xkey], df[ykey], legend= labelDict[ykey],
                line_width = 2, line_color=mycolors[i])

            figs.append(p1)

    #Store components 
    bigplot = column(*figs)
    script, div = components(bigplot)
    #except:
    #    print('Sheet plotting error')
    #    script,div = '',''
    return render(request, 'data/sheet_detail.html', {'sheet':sh,'data':df,'script':script,'div':div,
                                                      'list_diagnostics':ld})

labelDict = {'plasma_gas': 'PlasmaGas [g/s]', 'kurtlesker_pirani': 'KurtLeskerPirani [Pa]', 'gardon_temp': 'GardonTemp [degC]', 'pitot_temp': 'PitotTemp [degC]', 'cathode_supply': 'Cathode Supply [degC]', 'cathode_return': 'Cathode Return [degC]', 'pitot_position': 'PitotPosition [in]', 'voltage': 'Arc Voltage [V]', 'pitot_pressure': 'PitotPressure [Pa]', 'time': 'Time [s]', 'currentSC': 'CurrentSC [A]', 'vex_position': 'String Pot Vex [in]', 'current': 'Current [A]', 'shield_gas': 'ShieldGas [g/s]', 'gardon_heat_flux': 'GardonHeatFlux [W/cm^2]', 'B_RAX_pirani': 'B-RAX-Pirani [V]', 'gardon_position': 'GardonPosition [in]', 'chamber_pressure': 'ChamberPressure [Pa]', 'column_pressure': 'ColumnPressure [Pa]', 'vacuumpump_pressure': 'Vacuumpumps [Pa]', 'anode_deltaT': 'AnodeDeltaT [degC]'}

revLabelDict = {'PitotPressure [Pa]': 'pitot_pressure', 'ColumnPressure [Pa]': 'column_pressure', 'Arc Voltage [V]': 'voltage', 'Cathode Return [degC]': 'cathode_return', 'Time [s]': 'time', 'AnodeDeltaT [degC]': 'anode_deltaT', 'GardonTemp [degC]': 'gardon_temp', 'Vacuumpumps [Pa]': 'vacuumpump_pressure', 'B-RAX-Pirani [V]': 'B_RAX_pirani', 'Position [in]': 'gardon_position', 'ShieldGas [g/s]': 'shield_gas', 'String Pot Vex [in]': 'vex_position', 'GardonHeatFlux [W/cm^2]': 'gardon_heat_flux', 'PitotTemp [degC]': 'pitot_temp', 'Cathode Supply [degC]': 'cathode_supply', 'PlasmaGas [g/s]': 'plasma_gas', 'ChamberPressure [Pa]': 'chamber_pressure', 'KurtLeskerPirani [Pa]': 'kurtlesker_pirani', 'Position [in]': 'pitot_position', 'CurrentSC [A]': 'currentSC', 'Current [A]': 'current'}

colDict = {'time': 1, 'currentSC': 11, 'vacuumpump_pressure': 18, 'cathode_return': 9, 'voltage': 2, 'column_pressure': 5, 'pitot_position': 16, 'gardon_heat_flux': 14, 'shield_gas': 7, 'current': 3, 'gardon_position': 17, 'pitot_pressure': 13, 'vex_position': 19, 'B_RAX_pirani': 21, 'pitot_temp': 12, 'gardon_temp': 15, 'plasma_gas': 6, 'kurtlesker_pirani': 20, 'cathode_supply': 10, 'anode_deltaT': 8, 'chamber_pressure': 4}

mycolors = ['green','red','blue','cyan','orange','black','magenta','purple','olive','lime','yellow','gold','darkred','salmon','deeppink','coral','turquoise','teal','darkkhaki','khaki','navy','steelblue']
