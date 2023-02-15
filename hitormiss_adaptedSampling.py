'''
Evaluate the integral

\int_0^1 1/x**pp

utilizing adaptive sampling

'''
import numpy as np
import math as mt
import statistics as st
import pylab as pl  # useful to plot stuff!

# number of points we will consider

N_l = [1000, 2000, 4000, 8000, 16000, 32000]

P_in = 0.85
L_in = 0.81

# true value for safety checks
TT = 1. / (1.-P_in)

#print("True value: %s" % TT)

# vectors of results
Ar = []
Vr = []

# defines a function that, given a value of a variable
# and two powers, pp, ll, returns:
# the value of the function

def IntFun(XX, PP, LL):
	return 1./XX**(PP-LL)

# defines a function that, taken a number of points, the value of p, 
# and the value of \ell, returns:
# mean, variance
def Ip_est(NN, pp, ell):
	# p2 normalization
	NP2 = 1. / (1.-ell)
	# here we are using direct sampling of the distribution
	# p = 1/ x**p2
	# so we know that:
	# x  = u**(1/(1-p2))
	datax = (np.random.rand(NN))**(1. / (1.-ell))
	# generation of the result for the estimate
	YY = IntFun(datax,pp, ell)
	# mean
	A=NP2*np.sum(YY)/NN
	# error
	VV = st.variance(YY) / mt.sqrt(NN)
	#print("Number of points used: %s" % NN)
	#print("Value obtained: %s" % A)
	#print("Error: %s" % VV)
	return(A, VV)


for j in N_l:
	aa, vv = Ip_est(j, P_in, L_in)
	Ar.append(aa),
	Vr.append(vv)

np.savetxt("Output_%sP_%sL.txt" % (P_in,L_in),(N_l,Ar, Vr))
#print(Ar, Vr)


exit()