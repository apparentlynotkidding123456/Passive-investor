import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.pyplot import figure
import datetime
import pandas_datareader.data as web
from scipy.interpolate import interp1d


#check if margin multiplier is correct
#add margin monthly
#200 sma strat
#take out if loosing add if winning

Multiplier=1
Margin=1000
Fees=5.5 #Per contract

#Start and end times
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()
end = datetime.datetime(2021, 1, 1)

#Read data from yahoo finance
df = web.DataReader("SPY", 'yahoo', start, end) #SXR8.DE
Buyingpower=df.iloc[0][2]*Multiplier*10
Marginx=Buyingpower/Margin
#Get closing/low data
SPY = df[['Low']].to_numpy()
#Initialize Lists
SPY_diff =[]
#Calculate % differences between each day
#for i in range(1,len(SPY)):
#    SPY_diff.append(float(SPY[i]-SPY[i-1]))
x=0
n=1
Cum=[0]
z=[0]
prcnt=[]
for i in range(1,len(SPY)):
    x=x+1
    if x==21:
        y=float(SPY[i]-SPY[i-21])*n
        #print(SPY[i], ' - ', SPY[i - 21],' = ',y,' n = ',n)
        Cum.append(float(y+Cum[-1]))
        z.append(float(Margin+z[-1]))
        prcnt.append((Cum[-1]*Multiplier*100)/z[-1])
        #print(Cum[-1] * Multiplier * 100, ' divided by ', z[-1], ' = ',(Cum[-1]*Multiplier*100)/z[-1])
        x=0
        n=n+1


#plotting
plt.figure(1)
fig, ax=plt.subplots()

plt.plot(np.arange(0,len(SPY)),SPY,'g') #Index
ax2=ax.twinx().twiny()
plt.plot(np.arange(0,len(prcnt)),prcnt,'r') #Buy 1000 every month

x=0
n=1
Cum=[0]
z=[float(SPY[0])]
prcnt=[]
for i in range(1,len(SPY)):
    x=x+1
    if x==21:
        y=float(SPY[i]-SPY[i-21])*n
        #print(SPY[i], ' - ', SPY[i - 21],' = ',y,' n = ',n)
        Cum.append(float(y+Cum[-1]))
        z.append(float(SPY[i]+z[-1]))
        prcnt.append((Cum[-1]*100)/z[-1])
        x=0
        n=n+1

#plt.plot(np.arange(0,len(prcnt)),prcnt,'b') #buy 1 share every month

ax.xaxis.set_major_locator(MultipleLocator(20))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
plt.show()