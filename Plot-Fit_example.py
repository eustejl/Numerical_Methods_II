import math as mt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#parameters we are interested in
P_in = 0.85
L_in = 0.81

# load input
N_l, Ar, Vr = np.loadtxt("Output_%sP_%sL.txt" % (P_in,L_in))

## Fitting procedure is down in two steps:
## Step 1: identify the target function

def func(x, a, b):
    return a * x**b

## Step 2: perform the fit

popt, pcov = curve_fit(func, N_l, Vr)

print("Best fit with power: %s \n and prefactor %s " % (popt[1],  popt[0]))

#print("Best fit with power: %s (%s) \n and prefactor %s (%s)" % (popt[1], pcov[1], popt[0], pcov[0]))



## Plotting routines

plt.loglog(N_l, Vr, 'o', label='Error')
plt.loglog(N_l, func(N_l, *popt), '-', label='Fit (a+x^b), b=%.4f' % popt[1])

plt.legend(loc=1,fontsize=15)
#plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

plt.xlabel("Number of points",fontsize=15)
plt.ylabel("Error",fontsize=15)
#plt.semilogx(L_list,At_tau)
plt.savefig('Plot_Fit_%sP_%sL.png' % (P_in,L_in))