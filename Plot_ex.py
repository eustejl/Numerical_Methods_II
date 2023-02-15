import math as mt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


#parameters we are interested in
P_in = 0.85
L_in = 0.81

# load input
N_l, Ar, Vr = np.loadtxt("Output_%sP_%sL.txt" % (P_in,L_in))

def func(x, a, b):
    return a * x**b

plt.plot(N_l, Vr, 'o', label='Error scaling')
plt.legend(loc=1,fontsize=15)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

plt.xlabel("Number of points",fontsize=20)
plt.ylabel("Error",fontsize=20)
#plt.semilogx(L_list,At_tau)
plt.savefig('Plot.png')