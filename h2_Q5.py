import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

def f(x,y):
    return 2*x - 2*np.log(y)


k = np.linspace(0,10,10)

l = np.linspace(0,1.5,100)

K, L =np.meshgrid(k, l)

Z = f(K,L)

fig = plt.figure()

ax = plt.axes(projection = '3d')

graph1 = ax.contour3D(K,L,Z,50)

plt.show()
