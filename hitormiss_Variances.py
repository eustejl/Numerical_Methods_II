'''
Evaluate the Area of a circle of radius 1, pi * r**2.
Using numpy arrays in parallel

Once data are generated, computes variances

Challenge: make the code more efficient / why is it very slow?
'''

import numpy as np
import math as mt
import pylab as pl  # useful to plot stuff!

# number of points we will draw
NN = 1000
# minimum set we consider for our analysis
n_min = 100
# NN rows of data, with two values each, x and y
data = np.random.rand(NN,2)

xs = data[:,0]
ys = data[:,1]
# A boolean array where x^2 + y^2 < 1:
hits = xs**2 + ys**2 < 1.0

Av = []
dA_sq = []
Var = []
Sigma = []

# Computation of the average
A = float(4 * np.count_nonzero(hits)) / NN

#computation of the differences 
for j in range(n_min, NN):
    # Computation of the average at fixed NN	
    AV_n = float(4 * np.count_nonzero(hits[0:j])) / j
    Av.append(AV_n)
    dA = 0
    for k in range(0, j):
    #computation of the 
        dA += (float(4 * np.count_nonzero(hits[k]) - AV_n))**2
    Var.append(dA)
    Sigma.append(mt.sqrt(dA / (j * (j+1))))



Err = Sigma[NN-(n_min+1)]

# area in one quarter
#A = float(4 * np.count_nonzero(hits)) / NN

Exp = (A - mt.pi)

print("Number of points used: %s" % NN)
print("Value obtained: %s" % A)
print("Error versus expected value: %s" % Exp)
print("Estimated error: %s" % Err)

x_vec = np.arange(NN)

pl.title('Standard deviations')

# generate a reference line with 1/\sqrt{x}
xspace = np.linspace(NN/100., NN, NN)
#pl.loglog(1./np.sqrt(xspace),'bd', label='Reference line')

pl.loglog(Sigma,'r-', label='Stand. Dev.')
pl.loglog(1./np.sqrt(xspace),'bd', label='Square root scaling')
pl.loglog(1./(xspace),'g.', label='Linear scaling')

pl.xlabel('step')
pl.ylabel('$\sigma$')
pl.xlim(10, NN)
#pl.ylim(min(sigma_vec), max(sigma_vec))
pl.legend()

pl.savefig('EstimateCirle.png')

pl.show()