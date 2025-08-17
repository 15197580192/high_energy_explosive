# 求解水下冲击波能，冲击波压力峰值，冲量

import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.interpolate import interp1d


def find_roots(x,y):
    s = np.abs(np.diff(np.sign(y))).astype(bool)
    return x[:-1][s] + np.diff(x)[s]/(np.abs(y[1:][s]/y[:-1][s])+1) 

with open('w-p-t-1-1.0m.txt') as infile:
  datain=infile.readlines()[8:]
  
  r0 = 1.0 ; rho_w=1025.0; c_w = 1647.0; m_w=26/1000.0
  coef= 4.0*math.pi*r0**2
  coef = coef/m_w/rho_w/c_w
  
#drop last line endcurve
datain.pop()
x = [float(line.split()[0]) for line in datain]
y = [float(line.split()[1]) for line in datain]

y= np.asarray(y)

y0=np.max(y)/np.e
z = find_roots(np.asarray(x),np.asarray(y)-y0 )

#print(z)

#plt.plot(np.diff(x))
#plt.show()

max_idx = np.argmax(y)

print('peak idx',max_idx)

print('time of maximum pressure',x[np.argmax(y)],'mus')

print(' maximum pressure',np.max(y)*10**5,'MPa')
      
print('time of P_max/e',z[1],'mus')



theta=z[1]-x[np.argmax(y)]
print('theta is: ',theta,'mus')

# prepare integration	
tau=z[0]
print(' tau choosed as P_max/e mid of ascent', tau,'mus')
print('6.7*theta+tau = ', 6.7*theta+tau, 'mus')

idx_up=np.abs(x-(6.7*theta+tau)).argmin()
impulse=np.trapz(y[:idx_up+1],x[:idx_up+1])*10**2
print('impulse is :',impulse,'kPa.s')


idx_tau=np.abs(x-tau).argmin()
impulse_tau = np.trapz(y[idx_tau:idx_up+1],x[idx_tau:idx_up+1])*10**2
print('impulse start from tau is :',impulse_tau, 'kPa.s')




energy_tau = np.trapz(np.square(y[idx_tau:idx_up+1]).tolist(),x[idx_tau:idx_up+1])

energy_tau = energy_tau*coef*10**10

print('Energy start from tau is :',energy_tau,'MJ/kg')


plt.plot(x ,y)

plt.plot(z, y0*np.ones(len(z)), marker="o", ls="", ms=4)

plt.axhline(y=y0, xmin=0, xmax=2000,ls='dashdot')

plt.axvline(x=x[idx_tau], ymin=0.01, ymax=2,ls='dashdot')
plt.axvline(x=x[idx_up], ymin=0.01, ymax=2,ls='--')

plt.show()