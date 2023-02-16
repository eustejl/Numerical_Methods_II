import numpy as np
import matplotlib.pyplot as plt

def int_func(x1,x2,x3,x4,sigma):
    ss = ((x1**2)+(x2**2)+(x3**2)+(x4**2))**2
    return (np.sin((np.pi/2)*ss))*(np.exp(-ss/sigma))