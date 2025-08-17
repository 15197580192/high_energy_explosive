import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import interp1d

time = 490/1000
mw_c = 45; mw_ap= 35; mw_al= 100- mw_c-mw_ap

radius_c = 120; radius_ap = 120; radius_al = 13

rho_c = 2.04; rho_ap = 1.954; rho_al = 2.102

frac_cap = 0.1; frac_cal = 0.6; frac_cc = 1.0- frac_cap - frac_cal

frac_apap = 0.7; frac_apal = 1.0 - frac_apap - frac_cap  #totoal is 1

kcc = 13; kcap = 12; kcal= 35

kapap = 18.0; kapal = 15; kalal = 8

sem_c = 0.0; sem_ap =0.0; sem_al = 0.0

sem_c = 3.0 /(rho_c* radius_c)

sem_ap = 3.0 /(rho_ap * radius_ap)

sem_al = 3.0 /(rho_al * radius_al)

# 归一化过程

print("sem", sem_c, sem_ap,sem_al)

sum_c = sem_c/ (sem_c + sem_ap + sem_al)

sum_ap = sem_ap/ (sem_c + sem_ap + sem_al)

sum_al = sem_al / (sem_c + sem_ap + sem_al)

print("sum", sum_c, sum_ap,sum_al)

sem_cap = sum_c * frac_cap; sem_cal = sum_c * frac_cal
sem_cc = frac_cc * sum_c

sem_apap = sum_ap  * frac_apap

sem_apal = sum_ap *abs(1.0-frac_apap-frac_apal)

sem_alal = sum_al* abs(1.0-frac_cal-frac_apal)



print("sem_c",sem_cc,sem_cap, sem_cal)
print("sem_ap",sem_cap,sem_apap, sem_apal)
print("sem_al",sem_cal,sem_alal, sem_apal)
print("frac_cap",1.0-frac_apap-frac_apal)
print("frac_alal",1.0-frac_cal-frac_apal)


#d lambda_c/ dt = kcc*(1.0-lambda_c)*sem_cc + kcal*(1.0 - lambda_c)*sem_cal + kcap*(1.0 - lambda_c)*sem_cap

lambda_c = 1.0 - math.exp ( - (kcc*sem_cc + kcal*sem_cal + kcap *sem_cap)*time) 

lambda_ap = 1.0 - math.exp ( - (kapap*sem_apap + kapal*sem_apal + kcap *sem_cap)*time)

lambda_al = 1.0 - math.exp ( - (kcal*sem_cal + kapal*sem_apal + kalal *sem_alal)*time)
 
print("lambda", lambda_c, lambda_ap, lambda_al) 
 
print("lambda", lambda_c) 
#d lambda_ap/ dt = kapap*(1.0-lambda_ap)*sem_apap+ kcap*(1.0 - lambda_ap)*sem_cap + kapal*(1.0 - lambda_ap)*sem_apal

#d lambda_al/ dt = kalal*(1.0-lambda_al)*sem_alal+ kcal*(1.0 - lambda_al)*sem_cal + kapal*(1.0 - lambda_al)*sem_apal