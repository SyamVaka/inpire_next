import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pulp import *
import matplotlib.pyplot as plt

PRED_DATA = "D:\\python\\test.csv"

df = pd.read_csv(PRED_DATA)
df.head()

listofCells=["Cell_000112","Cell_001803","Cell_002303","Cell_003781","Cell_003793","Cell_004083","Cell_039873"]


#df[df['CellName']=="Cell_000111"]
   
dfObj1 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
dfObj2 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
dfObj3 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
dfObj4 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
dfObj5 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
dfObj6 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])
dfObj7 = pd.DataFrame(columns=['Date','Hour','CellName','Traffic'])

dfObj1=dfObj1.append(df[df['CellName']== listofCells[0]])
dfObj2=dfObj2.append(df[df['CellName']== listofCells[1]])
dfObj3=dfObj3.append(df[df['CellName']== listofCells[2]])
dfObj4=dfObj4.append(df[df['CellName']== listofCells[3]])
dfObj5=dfObj5.append(df[df['CellName']== listofCells[4]])
dfObj6=dfObj6.append(df[df['CellName']== listofCells[5]])
dfObj7=dfObj7.append(df[df['CellName']== listofCells[6]])

dfObj1['Traffic']=dfObj1['Traffic'].apply(lambda x: x/10.0) 
dfObj2['Traffic']=dfObj2['Traffic'].apply(lambda x: x/10.0)
dfObj4['Traffic']=dfObj4['Traffic'].apply(lambda x: x/10.0)
dfObj5['Traffic']=dfObj5['Traffic'].apply(lambda x: x/10.0)
dfObj6['Traffic']=dfObj6['Traffic'].apply(lambda x: x/10.0)
dfObj7['Traffic']=dfObj7['Traffic'].apply(lambda x: x/10.0)


df=[dfObj1,dfObj2,dfObj3,dfObj4,dfObj5,dfObj6,dfObj7]

for d in df:
    d['OptTraffic']=np.nan

Pds_M = 100
Ppa_M = 156
Pt_M = 100

Pds_m1 = 100
Ppa_m1 = 16.6
Pt_m1 = 100

Pds_f = 7.9
Ppa_f = 2.4
Pt_f =  1.8

maxMacroL = 6500
maxMicroL = 650

dfPow = pd.DataFrame(columns=['Sno', 'ActPower', 'OptPower'])

def func(i):
    prob = LpProblem("power_L", LpMinimize)

    L1 = LpVariable("L1",lowBound=0)
    L2 = LpVariable("L2",lowBound=0)
    L3 = LpVariable("L3",lowBound=1)
    L4 = LpVariable("L4",lowBound=0)
    L5 = LpVariable("L5",lowBound=0)
    L6 = LpVariable("L6",lowBound=0)
    L7 = LpVariable("L7",lowBound=0)

    prob += ((L1*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (L2*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (L3*(Pds_M + Ppa_M + Pt_M )/maxMacroL) + \
             (L4*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (L5*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL)+ \
             (L6*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (L7*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL))

    #lst = [865.37949, 96.7707, 651.8328700000001, 3354.72987, 195.54437]
    param = [dfObj1['Traffic'].iloc[i],dfObj2['Traffic'].iloc[i],dfObj3['Traffic'].iloc[i],dfObj4['Traffic'].iloc[i],
             dfObj5['Traffic'].iloc[i],dfObj6['Traffic'].iloc[i],dfObj7['Traffic'].iloc[i]]
    prob += L3 + L1 == (param[2] + param[0])
    prob += L3 + L2 == (param[2] + param[1])
    prob += L3 + L4 == (param[2] + param[3])
    prob += L3 + L5 == (param[2] + param[4])
    prob += L3 + L6 == (param[2] + param[5])
    prob += L3 + L7 == (param[2] + param[6])
    prob += L3 <= maxMacroL

#    print(prob)

    status = prob.solve()
 #   print(LpStatus[status])
 #   print(value(L1))
 #   print(value(L2))
 #   print(value(L3))
 #   print(value(L4))
 #   print(value(L5))


    power_act = ((param[0]*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (param[1]*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (param[2]*(Pds_M + Ppa_M + Pt_M )/maxMacroL) + \
             (param[3]*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (param[4]*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL)+ \
             (param[5]*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (param[6]*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL))    
    power_opt = ((value(L1)*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (value(L2)*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (value(L3)*(Pds_M + Ppa_M + Pt_M )/maxMacroL) + \
             (value(L4)*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (value(L5)*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL)+ \
             (value(L6)*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL) + \
             (value(L7)*(Pds_m1 + Ppa_m1 + Pt_m1)/maxMicroL))
    print(power_act, "  ",power_opt)
    dfObj1['OptTraffic'].iloc[i]=value(L1)
    dfObj2['OptTraffic'].iloc[i]=value(L2)
    dfObj3['OptTraffic'].iloc[i]=value(L3)
    dfObj4['OptTraffic'].iloc[i]=value(L4)
    dfObj5['OptTraffic'].iloc[i]=value(L5)
    dfObj6['OptTraffic'].iloc[i]=value(L6)
    dfObj7['OptTraffic'].iloc[i]=value(L7)
    return [power_act, power_opt]
ind = 0
for i in range(0,dfObj1.shape[0]):    
        ret = func(i)
        dfPow = dfPow.append({'Sno':i, 'ActPower': ret[0], 'OptPower': ret[1]}, ignore_index=True)   

#print(total_power_actual - total_power_opt)            
print(dfPow.head())
dfPow.to_csv('D:\\python\\pow2.csv', index=False)


for i in range(0,len(df)):
    if i==2:
        powf=(Pds_M + Ppa_M + Pt_M )
        maxL=maxMacroL
    else:
        powf=(Pds_m1 + Ppa_m1 + Pt_m1)
        maxL=maxMicroL
        
    df[i]['ActPower']=df[i]['Traffic'].apply(lambda x: (x*powf/maxL))
    df[i]['OptPower']=df[i]['OptTraffic'].apply(lambda x: (x*powf/maxL))
    filen='D:\\python\\'+listofCells[i]+'_pow.csv'
    df[i].to_csv(filen, index=False)
    
 






