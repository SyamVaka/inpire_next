import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pulp import *
import matplotlib.pyplot as plt

PRED_DATA = "D:\\python\\test.csv"

df = pd.read_csv(PRED_DATA)
df.head()

listofCells=["Cell_000111","Cell_000112","Cell_000113","Cell_001791","Cell_001792"]


df[df['CellName']=="Cell_000111"]
   
dfObj = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
for cell in listofCells:
    dfObj=dfObj.append(df[df['CellName']== cell])
dfObj.head()

max(dfObj['Traffic'])

hours=list(dfObj.Hour.unique())
hours
dates=list(dfObj.Date.unique())
dates

lst=[]

for date in dates:
    for hour in hours:
        lstI=[]
        for i, row in dfObj.iterrows():
            if ((row['Date'] == date) and (row['Hour'] == hour)):
                lstI.append(row['Traffic'])
        lst.append(lstI)    

from scipy.optimize import minimize

Pds_M = 100
Ppa_M = 156
Pt_M = 100

Pds_m1 = 100
Ppa_m1 = 16.6
Pt_m1 = 100

Pds_f = 7.9
Ppa_f = 2.4
Pt_f =  1.8

maxL = 6500

dfPow = pd.DataFrame(columns=['Sno', 'ActPower', 'OptPower'])

def func(param):
    prob = LpProblem("power", LpMinimize)

    L1 = LpVariable("L1",lowBound=1)
    L2 = LpVariable("L2",lowBound=0)
    L3 = LpVariable("L3",lowBound=0)
    L4 = LpVariable("L4",lowBound=0)
    L5 = LpVariable("L5",lowBound=0)

    prob += ((L1*(Pds_M + Ppa_M + Pt_M )+ L2*(Pds_m1 + Ppa_m1 + Pt_m1) + \
             L3*(Pds_m1 + Ppa_m1 + Pt_m1) + L4*(Pds_m1 + Ppa_m1 + Pt_m1) \
             + L5*(Pds_f + Ppa_f + Pt_f))/maxL)

    #lst = [865.37949, 96.7707, 651.8328700000001, 3354.72987, 195.54437]

    prob += L1 + L2 == (param[0] + param[1])
    prob += L1 + L3 == (param[0] + param[2])
    prob += L1 + L4 == (param[0] + param[3])
    prob += L1 + L5 == (param[0] + param[4])
    prob += L1 <= maxL

#    print(prob)

    status = prob.solve()
 #   print(LpStatus[status])
 #   print(value(L1))
 #   print(value(L2))
 #   print(value(L3))
 #   print(value(L4))
 #   print(value(L5))


    power_act = ((param[0]*(Pds_M + Ppa_M + Pt_M )+ param[1]*(Pds_m1 + Ppa_m1 + Pt_m1) + \
                param[2]*(Pds_m1 + Ppa_m1 + Pt_m1) + param[3]*(Pds_m1 + Ppa_m1 + Pt_m1) \
                + param[4]*(Pds_f + Ppa_f + Pt_f))/maxL)
    
    power_opt = ((value(L1)*(Pds_M + Ppa_M + Pt_M )+ value(L2)*(Pds_m1 + Ppa_m1 + Pt_m1) + \
                 value(L3)*(Pds_m1 + Ppa_m1 + Pt_m1) + value(L4)*(Pds_m1 + Ppa_m1 + Pt_m1) \
                 + value(L5)*(Pds_f + Ppa_f + Pt_f))/maxL)
    print(power_act, "  ",power_opt)
    return [power_act, power_opt]
ind = 0
for param in lst:    
        if(len(param) == 5):
            ind = ind+1
            ret = func(param)
            dfPow = dfPow.append({'Sno':ind, 'ActPower': ret[0], 'OptPower': ret[1]}, ignore_index=True)   

#print(total_power_actual - total_power_opt)            
print(dfPow.head())
dfPow.to_csv('D:\\python\\pow2.csv', index=False)

df.plot(legend=False)
