# Reading Excel files
import pandas as pd
import matplotlib.pyplot as plt
from numpy import shape, array, arange,zeros,ones,nan
from os import listdir
from os.path import isfile, join
from data.models import *
import datetime

path = "/home/magnus/Dropbox/ARCJET/mARC/data/"
fnames = [f for f in listdir(path) if isfile(join(path, f))]

print(fnames)
input('Continue? ')

columnheaders = [['Time [s]','Time*'],
                 ['Arc Voltage [V]','Arc Voltage', 'ArcVolt', 'ArcVolt [V]', 'ArcVolt_V7_mod3_ai18_(0-10V)'],
                 ['Current [A]','Current','Current_mod2_ai1'],
                 ['ChamberPressure [Pa]','Cham Pres_terra [torr]_mod2_ai2', 'Chamber Pres [Pa]', 'Chamber Pres [kPa]-Mod3_ai4', 'ChamberTC01-cDAQ1Mod4_ai9', 'ChamberTC11-cDAQ1Mod4_ai7', 'ChamberTC12-cDAQ1Mod4_ai8', 'Chamberpres [kPa]', 'Chamberpres[kPa]'],
                 ['ColumnPressure [Pa]','ColPres [Pa]', 'ColPres [Pa]_mod1_ai0', 'Colpres [torr]', 'Colpres[torr]', 'Colpres[torr]-Mod3-ai5', 'Column Pressure [kPa]'],
                 ['PlasmaGas [g/s]', 'PlasmaGas[g/s]', 'PlasmaGas[g/s]_mod3_ai7_V5 (0-10V)'],
                 ['ShieldGas [g/s]', 'ShieldGas[g/s]', 'ShieldGas[g/s]_mod3_ai17_V6 (0-10V)'],
                 ['AnodeDeltaT [degC]','Anode DeltT [C]'],
                 ['Cathode Return [degC]','Cathode Return [C]', 'CathodeRet [degC]'],
                 ['Cathode Supply [degC]','Cathode Supply[C]', 'CathodeSup [degC]'],
                 ['CurrentSC [A]', 'CurrentSC[A]-Mod4_ai6', 'Current_SC', 'Mod4_ai6_curSC [A]'],
                 ['PitotTemp [degC]','EndevcoTemp [degC]','Endevco Tempt [C]', 'EndevcoTempt [degC]', 'EndevcoTempt[K]'],
                 ['PitotPressure [Pa]','EndevcoStagPres[Pa]','EndevcoStagPres [kPa]', 'EndevcoStagPres[Pa]_mod3_ai6_V4 (0-1V)', 'Pitotpres [Pa]', 'Stag Pressure [kPa]'],
                 ['GardonHeatFlux [W/cm^2]','GGhf', 'GGhf [w/cm^2]', 'GGhf[W/cm^2]', 'GGhf[W/cm^2]_mod4_ai1'],
                 ['GardonTemp [degC]','GG_Tempt', 'GGtempt', 'GGtempt [degC]', 'GGtempt[deg.C]', 'Gardontempt [degC]'],
                 ['PitotPosition [in]','String Pot_Pitot', 'String Pot_Pitot [in]_mod3_ai19', 'SPot_Pitot [in]', 'Pitotpos [in]'],
                 ['GardonPosition [in]','StringPot_Gardon', 'StringPot_Gardon[in]_mod3_ai23', 'SPot_Gardon[in]', 'Gardonpos [in]'],
                 ['Vacuumpumps [Pa]','Vacuumpumps [kPa]', 'Vacuumpumps[kPa]'],
                 ['String Pot Vex [in]','String Pot Vex', 'String Pot Vex_mod3_ai20'],
                 ['KurtLeskerPirani [Pa]','kurtleskerpirani[Pa]', 'kurtleskerpirani[Pa]_mod1_ai2'],
                 ['B-RAX-Pirani [V]','B-RAX-Pirani[V]mod3_ai5_V3 (0-10V)']
           ]

units = {'[degC]':[0,1,'[degC]'],'[deg.C]':[0,1,'[degC]'],'GG_Tempt':[0,1,'[degC]'],'GGtempt':[0,1,'[degC]'],'[C]':[0,1,'[degC]'],'[K]':[273,1.,'[degC]'],
         '[V]':[0,1,'[V]'],'Volt':[0,1,'[V]'],
         '[A]':[0,1,'[A]'],'Current':[0,1,'[A]'],
         '[Pa]':[0,1,'[Pa]'],'[kPa]':[0,1000,'[Pa]'],'[torr]':[0,133.32,'[Pa]'],
         '[W/cm^2]':[0,1,'[W/cm^2]'],'[w/cm^2]':[0,1,'[W/cm^2]'],'GGhf':[0,1,'[W/cm^2]'],
         '[g/s]':[0,1,'[g/s]'],'[in]':[0,1,'[in]'],'Pot':[0,1,'[in]'],
         'Time*':[0,1,'[s]']}


for fname in ['08-07-17_n2_co2.xlsx']:
    print('###########################################\n\n'+fname+'\n')
    xl = pd.ExcelFile(path+fname)
    yr,mon,day = int('20'+fname[6:8]), int(fname[0:2]),int(fname[3:5])

    ### Retrieve or create spreadsheet object
    query = Spreadsheet.objects.filter(filename=fname)
    if len(query) ==1:
        s = query[0]
    else:
        try:
            s = Spreadsheet(filename=fname,date = datetime.date(yr,mon,day))
            s.save()
        except:
            print(sn,"could not save")
    
    # Print the sheet names
    sheets = xl.sheet_names

    sheet_data=[]
    for sn in sheets:
        df = xl.parse(sn)
        if fname == '08-07-17_n2_co2.xlsx':
            mycols = df.values[1,:]
            print(mycols)
            mydata = df.values[2:,:]
            print(mydata[2:4,:])
        else:
            mycols = df.columns
            mydata = df.values
        print("*** "+sn, len(mycols))

        n = shape(mydata)[0]
        myarray = zeros((n,len(columnheaders)))
        boolarray =['1']*(len(columnheaders))
        ### loop through each desired column
        for i in range(0,len(columnheaders)):
            clist = columnheaders[i]

            ### search through sheet columns to find if column is present
            for j in range(0,len(mycols)):
                found = False
                if mycols[j] in clist:
                    found = True
                    ### parse units
                    for key in units:
                        if key in mycols[j]:
                            #print(mycols[j],key,clist)
                            myarray[:,i] = mydata[:,j]*units[key][1] + units[key][0] ### standardize units
                            break
                    break

            if not found:
                print("Not found: ",clist[0])
                boolarray[i]='0'
                myarray[:,i] = nan
        cboolstr = "".join(boolarray)

        print(cboolstr)

        query = Sheet.objects.filter(name=sn,spreadsheet=s)
        if len(query) ==1:
            sh = query[0]
##            sh.columnBooleans=cboolstr
##            sh.save()
        else:
            try:
                sh = Sheet(name=sn,spreadsheet=s,columnBooleans=cboolstr)
                sh.save()
            except:
                print(sn,"could not save")

        for row in range(0,len(myarray)):
            r = Record(spreadsheet=s,sheet=sh,
                   time=myarray[row,0],
                   voltage =myarray[row,1],
                   current = myarray[row,2],
                   chamber_pressure =myarray[row,3],
                   column_pressure  = myarray[row,4],
                   plasma_gas = myarray[row,5],
                   shield_gas = myarray[row,6],
                   anode_deltaT = myarray[row,7],
                   cathode_return = myarray[row,8],
                   cathode_supply =  myarray[row,9],
                   currentSC =  myarray[row,10],
                   pitot_temp =  myarray[row,11],
                   pitot_pressure =  myarray[row,12],
                   gardon_heat_flux = myarray[row,13],
                   gardon_temp =  myarray[row,14],
                   pitot_position =  myarray[row,15],
                   gardon_position =  myarray[row,16],
                   vacuumpump_pressure =  myarray[row,17],
                   vex_position =  myarray[row,18],
                   kurtlesker_pirani =  myarray[row,19],
                   B_RAX_pirani =  myarray[row,20])
            try:
                r.save()
            except:
                print(s,sn,r,"could not save")
                   
