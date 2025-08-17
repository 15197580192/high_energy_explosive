import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import interp1d


#  initial guess for r1, r2, omega
r1 = 6.88; r2 = 2.19; omega = 0.25

gamma= 2.2; rho_0 = 1920

pcj = 24.0; dcj = 7026.0; e0 =9.67

Q0 = 7003.0*10**3

#gamma = math.sqrt(dcj**2/2.0/Q0 +1); 

gamma = (rho_0*dcj**2)*10**(-9)/pcj - 1.0



vcj = gamma/(gamma+1)
print(vcj)



a11 = math.exp (-r1*vcj)/r1; a12 = math.exp(-r2*vcj)/r2
a13=vcj**(-omega)/omega

a21 = math.exp(-r1*vcj); a22 = math.exp (-r2*vcj); a23 = vcj**(-omega-1) 

a31 = r1*math.exp(-r1*vcj); a32 = r2*math.exp(-r2*vcj)
a33 = (omega+1)*vcj**(-omega-2)

y1 = e0 + 0.5*pcj*(1-vcj); y2 = pcj; y3 = rho_0 * (dcj**2)*(10**(-9))

 ##################################
 ## y1 = Q0 + 0.5*pcj*(1-vcj); y2 = pcj; y3 = rho_0 * dcj**2 * 10**(-9)

 ########################################################################################################

M = np.array([[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]])

Y= np.array([y1,y2,y3])

X=np.linalg.solve(M,Y)

print(X)




