import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True

x_light = [0.1, 1.0, 10.0, 20.0, 100.0]
y_light = [-0.1, -15.9, 4.9, 8.3, 20.9]
err_light = [0.0, 3.4, 3.8, 2.5, 2.1]
x_dark = [0.1, 1.0, 2.0, 10.0, 20.0, 100.0]
y_dark = [-0.1, -6.0, -2.9, 15.5, 17.7, 19.8]
err_dark = [0.0, 2.3, 4.5, 5.5, 3.0, 0.0]

pylab.figure(1,figsize=(5,4))
ax = pylab.axes((0.15,0.15,0.8,0.8))
ax.set_xscale('log')
pylab.errorbar(x_light,y_light,yerr=err_light,color='k',marker='o',markersize=10,linestyle='-',linewidth=2)
pylab.errorbar(x_dark,y_dark,yerr=err_dark,color='0.75',marker='o',markersize=10,linestyle='-',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.ylabel(r"\% change in $\omega_{ij}$")
pylab.xlabel(r"Stimulation frequency")
bbox_props = dict(boxstyle='square',fc='w',ec='0.5')
pylab.text(10,-10,'Light-reared',color='k',ha='center',va='center',size=12,bbox=bbox_props)
pylab.text(1,10,'Dark-reared',color='0.75',ha='center',va='center',size=12,bbox=bbox_props)
pylab.axis((0.07,150.0,-20.0,30.0))

if save:
  pylab.savefig('freq_dependence.pdf')
else:
  pylab.show()

