'''
Evaluate the Area of a circle of radius 1, pi * r**2.
Using numpy arrays in parallel

Plot the running average to have an idea about convergence
'''

import numpy as np
import math as mt
import matplotlib.pyplot as plt

# number of points we will draw
NN = 1000
# minimal number of points to start our plot
N_Start = int(NN*0.1)
# NN rows of data, with two values each, x and y
data = np.random.rand(NN,2)
# remember: rand has support [0, 1[
# helpful slices
xs = data[:,0]
ys = data[:,1]

# Array of data
Area = []

# A boolean array where x^2 + y^2 < 1:
# condition: is our point inside the circle or outside?
hits = xs**2 + ys**2 < 1.0

# Counter
CC = 0

# computing running average 
for j in range(NN):
    CC += float(4 * np.count_nonzero(hits[j])) 
    Area.append(CC / (j+1))

# this is just a check, since we know that the 
# final result is pi.
Exp = (float(CC/NN) - mt.pi)

print(CC)



print("Number of points used (total pinballs): %s" % NN)
print("Value obtained: %s" % float(CC/NN))
print("Error versus expected value: %s" % Exp)

#plt.plot(Area[N_Start:NN])

#plt.show()

exit()