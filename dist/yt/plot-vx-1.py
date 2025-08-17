#求解圆筒速度，格尼能
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def find_roots(x,y):
    s = np.abs(np.diff(np.sign(y))).astype(bool)
    return x[:-1][s] + np.diff(x)[s]/(np.abs(y[1:][s]/y[:-1][s])+1)
    
    

with open('yt-rx-t.txt') as infile:
  datain=infile.readlines()[8:]
  
#drop last line endcurve
datain.pop()
x = [float(line.split()[0]) for line in datain]
y = [float(line.split()[1]) for line in datain]


y0 = 1.9

# 19 mm
y-float(y0)*np.ones(len(y))
z = find_roots(np.asarray(x),np.asarray(y)-y0 )


print('time of this expansion: ',z)
#print(type(z))




# with open('yt-vx-t.txt') as infile:
with open('yt-rx-t.txt') as infile:
  datavin=infile.readlines()[8:]
  
#drop last line endcurve
datavin.pop()
xv = [float(line.split()[0]) for line in datavin]
yv = [float(line.split()[1]) for line in datavin]
 
 
interp_func = interp1d(xv, yv)
vt=interp_func(float(z[0]))

print('velocity of expansion: ',vt)


#mass of the container
m1=77.409
#mass of the explosive
m2=40.841

#energy of gurney
e_gurney=(1/2+m1/m2)*(vt**2)/2
print('energy of gurney: ',e_gurney)


gurney_p = (2*e_gurney)**0.5
print('gurney para is: ',gurney_p)





plt.subplot(2, 1, 1)
plt.plot(x ,y)

plt.plot(z, y0*np.ones(len(z)), marker="o", ls="", ms=4)






#todo draw line 19mm
plt.axhline(y=1.9, xmin=0, xmax=50,ls='dashdot')
#plt.axvline(x=5, ymin=0.1, ymax=0.9)





plt.title('rx by time')



plt.subplot(2, 1, 2)
plt.plot(xv ,yv)
plt.axvline(x=float(z[0]), ymin=0.01, ymax=2,ls='dashdot')

plt.plot(float(z[0]), vt , marker="o", ls="", ms=4)

plt.title('vx by time')

plt.show()



