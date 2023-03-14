__author__ = "JL Euste"

import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt


# =============================================================================
# Extract data from HISTORY FILE
# =============================================================================

start_init,end_init = 7,41 #start and end line numbers for initial frame
start_fin = 7967 # starting line number for the final frame
spacing = 6 #line spacing of coordinates of O
end_all = 8001 #last line in the file

coords_o_init,coords_o = [],[]
 
file = open('HISTORY') #open file
for i in range(end_all):
    line = file.readline()
    
    #extract coordinates of oxygen from the initial frame
    if i in np.arange(start_init,end_init,spacing): 
        coords_o_init.append(line)   
        
    #extract coordinates of oxygen from the final frame
    if i in np.arange(start_fin,start_fin+(end_init-start_init),spacing):        
        coords_o.append(line)

def coords_to_array(coords_list):
    ''' Change list of coordinates to array. '''
    n = len(coords_list)
    x = [float(coords_list[i][1:12]) for i in range(n)]
    y = [float(coords_list[i][14:24]) for i in range(n)]
    z = [float(coords_list[i][26:37]) for i in range(n)]  
    return np.array([x,y,z]).T
                
                
coords_o_init = coords_to_array(coords_o_init)
coords_o = coords_to_array(coords_o)


# =============================================================================
# Visualize
# =============================================================================
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot(coords_o_init[:,0],coords_o_init[:,1],coords_o_init[:,2],
        'o',label='initial')
ax.plot(coords_o[:,0],coords_o[:,1],coords_o[:,2],
        'o',label='final')
ax.legend()
plt.savefig('oxygen_init_vs_fin',bbox_inches='tight',dpi=300)
plt.show()
plt.close()

# =============================================================================
# Calculate pairwise distances using minimum image convention
# =============================================================================

def min_image(u,v,L=25.20):
    uv = u-v
    uv = uv - np.round(uv/L)*L
    return np.sqrt(np.sum(uv**2))

distances_o_init = pdist(coords_o_init,metric=min_image)
distances_o = pdist(coords_o,metric=min_image)

# =============================================================================
# Plotting
# =============================================================================

plt.hist(distances_o_init,density=True,label='initial')
plt.hist(distances_o,density=True,label='final')
plt.legend()
plt.xlabel('pairwise distance')
plt.ylabel('probability')
plt.savefig('radial_dist_oxygen_init_vs_fin',bbox_inches='tight',dpi=300)
plt.show()


