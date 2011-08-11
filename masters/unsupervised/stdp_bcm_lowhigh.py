import math
import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True
use_sub = True

pylab.figure(1,figsize=(7,4))
pylab.axes((0.1,0.2,0.85,0.7))
pylab.title(r"$\theta = 0.33$")
pylab.ylabel(r"$\Delta \omega_{ij} / \omega_{ij}$",fontsize=14)
pylab.xlabel(r"$t^{pre}-t^{post}$ (seconds)",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.hold(True)
execfile('data/theta0.33/pulse_delay_1hz/plot.py')
execfile('data/theta0.33/pulse_delay_40hz/plot.py')
pylab.axis((-0.03,0.021,-0.2,1.2))
pylab.legend()

if save:
  pylab.savefig('stdp_bcm_lowhigh.pdf')
else:
  pylab.show()

