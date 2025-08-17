import matplotlib.pyplot as plt
import numpy as np
import math

from scipy.signal import find_peaks
from scipy.signal import argrelextrema

rhow = 1025
mw= 0.02640
pw = 148500
with open('w-bubble.txt') as infile:
  datain=infile.readlines()[8:]
  
#drop last line endcurve
datain.pop()
x = [float(line.split()[0]) for line in datain]
y = [float(line.split()[1]) for line in datain]


#only for debug with random data
array_data = np.arange(start = 0, stop = 40, step = 1, dtype='int')
y_array_data = np.random.random(40)*5
#y=y_array_data
#x=array_data

#读取第一个波峰的y值即为最大气泡脉动半径(直接读取,单位为cm)



print("maximum of bubble is like ",np.max(y), "cm")

#pks,_ = find_peaks(y,height=0)
#print(pks)
#plt(pks,y[pks],"x")
#plt.plot(y)
#plt.show()

# to find all minima
minima_ind = argrelextrema(np.asarray(y), np.less)


#读取第一个的波谷的x值即为 第一次脉动周期数值Tb
# choose the first as pulse, minima_ind[0]
pulse1 = x[minima_ind[0][0]]
pulse2 = x[minima_ind[0][1]]
print("pulse Tb is like ",(pulse2-pulse1)/1000,pulse1,pulse2/1000, "ms")



# plot them
(fig, ax) = plt.subplots()
ax.plot(x,y)

print("index first of tuple minima: " , minima_ind[0][0])
#print(minima_ind) # as tuple	

x_minima = minima_ind[0]
y_minima = np.asarray(y)[minima_ind[0]]
ax.plot(x_minima, y_minima, marker='*', linestyle='dashed', color='green', label="Minima")

print("index of  maxima: " ,np.argmax(y)/1000,"ms")
tb = (2.0*np.argmax(y) + pulse2)/2000
print("cycle of tb", tb,"ms")
enetb = tb**3*pw**2.5*0.6839/mw/rhow**1.5*10**(-15)
print("cycle of tb energy", enetb,"MJ/kg")
ax.plot(np.asarray(x)[np.argmax(y)],np.max(y), marker='*', linestyle='dashed', color='orange', label="peaks")
plt.show()

