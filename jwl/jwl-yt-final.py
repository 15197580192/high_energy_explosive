# 这个是已知爆速，爆雅，暴热，猜测r1，r2，omega，求解a，b，c单位是GPa

import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

# f = [
#     [0.6, 0.42],
#     [0.8, 0.81],
#     [1.1, 0.9],
#     [2.0, 1.1],
#     [2.8, 1.2],
#     [3.0, 1.3],
#     [3.1, 1.45],
#     [19.0, 2.1]
# ]

# 从文件中读取数据
with open('data.txt', 'r') as file:
    lines = file.readlines()

data = [list(map(float, line.split())) for line in lines]
f = np.array(data)

  
f = np.array(f)
rad = f[:, 0]
ed = f[:, 1]



# 只用了rho_0,pcj,dcj
rho_0 = 1920.0

pcj = 22.0; dcj = 6817.0; e0 = 8.69  #注意单位换算

Q0 = 7003.0*10**3 


gamma = (rho_0*dcj**2)*10**(-9)/pcj - 1.0



vcj = gamma/(gamma+1)

print("vcj,gamma",vcj,gamma)

#v_6 = 2.4; v_19= 7.0;
rho_m = 1920.0; radius_0 = 25.4/2; x0 = 2.6

vrad = 1.0146 + 0.19174 * rad + 0.006178 * rad**2





#radius_6 = 15.7; x_6 = 3.1; theta_6 = 10.0/2.0/math.pi

#radius_19 = 21.7; x_19= 9.7;theta_19 = 11.6/2.0/math.pi

#gurney_v6 = 1.240*1000; gurney_v19 = 1.40*1000; gurney_v25 = 1.90*1000  #外壁径向移动速度

#ed_6=0
#ed_6 = ed_6 + rho_m * ((radius_6+x_6)/(radius_0))**2*math.log2((radius_6+x_6)/radius_6)

#ed_6 = ed_6 + rho_0*((radius_6+x_6)/radius_6)**2/4.0

#ed_6 = ed_6**2 * (gerney_v6*math.cos(theta_6))**2  # 固定的6mm
#ed_6 = ed_6**2 * (gurney_v6*math.cos(theta_6))**2  # 固定的6mm


#ed_19=0
#ed_19 = ed_19 + rho_m * ((radius_19+x_19)/(radius_0))**2*math.log2((radius_19+x_19)/radius_19)

#ed_19 = ed_19 + rho_0*((radius_19+x_19)/radius_19)**2/4.0

#ed_19 = ed_19**2 * (gerney_v19*math.cos(theta_19))**2  # 固定的19mm
#ed_19 = ed_19**2 * (gurney_v19*math.cos(theta_19))**2  # 固定的19mm

#RY(0) = e0-ed_6; RX(0) = v_6
#ed_25 = 0.0 

#ed_25 = 25.0
#RY(1) = e0-ed_19; RX(1) = v_19



def func(RX, r1, r2, omega):
   
    

   #  initial guess for r1, r2, omega
   # r1 = 4.58; r2 = 1.09; omega = 0.29

   a11 = math.exp (-r1*vcj)/r1; a12 = math.exp(-r2*vcj)/r2
   a13=vcj**(-omega)/omega

   a21 = math.exp(-r1*vcj); a22 = math.exp (-r2*vcj); a23 = vcj**(-omega-1) 

   a31 = r1*math.exp(-r1*vcj); a32 = r2*math.exp(-r2*vcj)
   a33 = (omega+1)*vcj**(-omega-2)

   y1 = e0 + 0.5*pcj*(1-vcj); y2 = pcj; y3 = rho_0 * (dcj**2)*(10**(-9))

 
   M = np.array([[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]])

   Y= np.array([y1,y2,y3])

   X=np.linalg.solve(M,Y)
#   print("x", X)
  
  
   return X[0]*np.exp (-r1*RX)/r1+ X[1]*np.exp(-r2*RX)/r2+X[2]*RX**(-omega)/omega

#Q0 = 7003.0*10**3

#gamma = math.sqrt(dcj**2/2.0/Q0 +1); 
#print(gamma)

##################################
## y1 = Q0 + 0.5*pcj*(1-vcj); y2 = pcj; y3 = rho_0 * dcj**2 * 10**(-9)


#RY = e0-ed_6; RX = v_6

#RY= e0-ed_19; RX = v_19

rx = vrad
ry = e0-ed*rho_m*10**(-3)
print("RX,RY",rx,ry)



initial_guess = [4.08, 1.09, 0.21]  # 这只是一个初步的猜测，可能需要根据数据进行调整
popt,_ = curve_fit(func, rx, ry, p0=initial_guess)

#print('error for 6mm: ',func(rx[0])-ry(0))

print('error for 19mm: ',rx[0]-ry[0])

print("parameter: ", popt)
estimated=func(rx,popt[0],popt[1],popt[2])

plt.plot(rx, ry, 'o', color ='red', label ="data")
plt.plot(rx, estimated, '--', color ='blue', label ="optimized data")
plt.legend()
plt.show()
####################################################










