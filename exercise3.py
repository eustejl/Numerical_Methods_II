'''
Numerical Methods II
Exercise 3
Lecture 5
Integral with Importance Sampling using Metropolis Algorithm
'''

__author__ = "JL Euste"


import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma,erf

np.random.seed(11)

sigmas = [0.1,1,10]

dim = 4 #dimensionality of the integral
solid_angle = 2*np.pi**(dim/2.)/gamma(dim/2.) #will be used from Cartesian to 4d spherical

def metropolis_integral(sigma,h,cyc=100,N_wup=5_000,N_meas=10_000,infty=True):
    def g(x):
        norm2 = np.sum(x**2)
        return (np.sin(np.pi*norm2/2))**2

    def p(x):
        norm2 = np.sum(x**2)
        return np.exp(-norm2/sigma)
    

    def to_update(x0,x1): #defines if we update or not
        a = min(1.,p(x1)/p(x0))
        
        if (a>=1.):  return x1 #accept
        else:
            r = np.random.random()
            if (r>a):   return x0 #reject
            else:   return x1 #accept
    
    if infty: #from -infinity to +infinity
        def markov_chain(x_in,cc): #Markov chain cycle
            for _ in range(cc):
                x_out = x_in + h*s_val*np.random.randn(dim)
                x_in = to_update(x_in,x_out)
            return x_in
        
        norm_fac = np.sqrt(np.pi*sigma)**dim #from normalization of p(x)
        
        #actual values from wolframalpha
        actual_vals = {0.1: 0.000633379*solid_angle,
                       1: 0.2687679475993*solid_angle,
                       10: 25.0252534*solid_angle} 
    else: #set infty to False if from 0 to 4
        def markov_chain(x_in,cc): #Markov chain cycle
            for _ in range(cc):
                x_out = x_in + h*np.random.randn(dim)/1000 #changed so <4
                x_in = to_update(x_in,x_out)
                
                #to ensure value within [0,4]
                if np.any(np.abs(x_in)>4): print('value out of bounds')
            return x_in
        
        norm_fac = (0.5*np.sqrt(np.pi*sigma)*erf(4/np.sqrt(sigma)))**dim #from normalization of p(x)
        
        #actual values from wolframalpha
        #divide by 16 because "quadrant" in 4D space
        actual_vals = {0.1: 0.000633379*solid_angle/16, 
                        1: 0.26876795*solid_angle/16,
                        10: 24.71809246*solid_angle/16}


    s_val = np.sqrt(sigma/2)    
    
    iters = np.arange(N_meas)
    int_res,stdevs = np.empty(N_meas),np.empty(N_meas)
    aa = []
    bb=0
    
    x0 = s_val*np.random.randn(dim) #initial guess
    x0 = markov_chain(x0,N_wup)
    
    for i in iters:
        x0 = markov_chain(x0,cyc)
        
        meas = g(x0)
        aa.append(meas)       	    
        	
        bb += meas #add this to the 'total' function
        int_res[i] = bb/(i+1) #new average value
        
        std = np.std(aa/np.sqrt(i+1)) #stdev
        stdevs[i] = std
        
    
   
    percent_dev = 100*abs(actual_vals[sigma]-norm_fac*bb/(i+1))/actual_vals[sigma]
    
    print(f'sigma={sigma}')
    print('Percent deviation from actual:',percent_dev) #change depending on sigma

    return iters,norm_fac*int_res,stdevs,actual_vals[sigma],percent_dev



# =============================================================================
# Full integral from -infinity to +infinity
# =============================================================================
fig,ax = plt.subplots(3,2,figsize=(12,16))
for i in range(len(sigmas)):
    sigma = sigmas[i]
    iters,int_res,stdevs,actual,percent_dev = metropolis_integral(h=1.5,
                                                                  sigma=sigma)
    ax[i,0].set_title('$\sigma$'+ f'={sigma}, %dev={percent_dev:.2f}')
    ax[i,0].errorbar(iters, int_res,yerr=stdevs,label='calculated')
    ax[i,0].plot(iters,np.full_like(iters,actual),'r--',label='actual')
    ax[i,0].legend()
    ax[i,0].set_ylabel('MC value',size='x-large')
    if i==(len(sigmas)-1): ax[i,0].set_xlabel('step',size='x-large')
    
    ax[i,1].set_title('Error')
    ax[i,1].loglog(iters,stdevs)
    ax[i,1].set_ylabel('$\sigma$',size='x-large')
    if i==(len(sigmas)-1): ax[i,1].set_xlabel('step',size='x-large')

fig.suptitle('Full integral from -inf to +inf')
fig.tight_layout()
plt.savefig('full_int')



# =============================================================================
# Proper integral from 0 to 4
# =============================================================================
fig,ax = plt.subplots(3,2,figsize=(12,16))
for i in range(len(sigmas)):
    h=1.5
    sigma = sigmas[i]
    if (sigma==1): h=0.06 #smaller so values within range [0,4]
    
    iters,int_res,stdevs,actual,percent_dev = metropolis_integral(h=h,
                                                                  sigma=sigma,
                                                                  infty=False)
    ax[i,0].set_title('$\sigma$'+ f'={sigma}, %dev={percent_dev:.2f}')
    ax[i,0].errorbar(iters, int_res,yerr=stdevs,label='calculated')
    ax[i,0].plot(iters,np.full_like(iters,actual),'r--',label='actual')
    ax[i,0].legend()
    ax[i,0].set_ylabel('MC value',size='x-large')
    if i==(len(sigmas)-1): ax[i,0].set_xlabel('step',size='x-large')
        
    ax[i,1].set_title('Error')
    ax[i,1].loglog(iters,stdevs)
    ax[i,1].set_ylabel('$\sigma$',size='x-large')
    if i==(len(sigmas)-1): ax[i,1].set_xlabel('step',size='x-large')

fig.suptitle('Proper integral from 0 to 4')
fig.tight_layout()
plt.savefig('proper_int_0_4')
