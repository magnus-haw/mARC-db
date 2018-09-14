# Query the database/compare to excel
import pandas as pd
import matplotlib.pyplot as plt
from numpy import shape, array, arange,zeros,ones,nan
from os import listdir
from os.path import isfile, join
from data.models import *
import datetime

path = "/home/magnus/Dropbox/ARCJET/mARC/data/"
fnames = [f for f in listdir(path) if isfile(join(path, f))]
mycols = ['time','voltage','current']
sh_ind = 0

fname = fnames[8]
print(fname)
input("Continue? ")

### Get database values
s= Spreadsheet.objects.get(pk=fname)
sh = Sheet.objects.filter(spreadsheet=s)
print(sh[sh_ind].name)
query = Record.objects.filter(spreadsheet=fname,sheet=sh[sh_ind]).values(*mycols)
mydata= array([[d['time'],d['voltage'],d['current']] for d in query])

plt.figure(0)
plt.plot(mydata[:,0],mydata[:,1],'bo')
plt.figure(1)
plt.plot(mydata[:,0],mydata[:,2],'bo')

### Get excel values
print('###########################################\n\n'+fname+'\n')
xl = pd.ExcelFile(path+fname)
sheets = xl.sheet_names
sn = sheets[sh_ind]
df = xl.parse(sn)
mycols = df.columns
exdata = df.values[2:,:]
print("*** "+sn, len(mycols))


t,v,a = exdata[:,0],exdata[:,2],exdata[:,3]

plt.figure(0)
plt.plot(t,v,'k-')

plt.figure(1)
plt.plot(t,a,'k-')
plt.show()
