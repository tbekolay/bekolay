import math
import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True
use_sub = True

pylab.figure(1,figsize=(10,10))
pylab.subplot(221)
pylab.title(r"5 Hz")
pylab.ylabel(r"$\Delta \omega_{ij} / \omega_{ij}$",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.axvline(linestyle='--',linewidth=1,color='k')
pylab.hold(True)
execfile('data/theta0.30/pulse_delay_5hz/plot.py')
execfile('data/theta0.33/pulse_delay_5hz/plot.py')
execfile('data/theta0.36/pulse_delay_5hz/plot.py')
pylab.axis((-0.03,0.021,-0.4,0.6))
pylab.legend()

pylab.subplot(222)
pylab.title(r"10 Hz")
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.axvline(linestyle='--',linewidth=1,color='k')
pylab.hold(True)
execfile('data/theta0.30/pulse_delay_10hz/plot.py')
execfile('data/theta0.33/pulse_delay_10hz/plot.py')
execfile('data/theta0.36/pulse_delay_10hz/plot.py')
pylab.axis((-0.03,0.021,-0.6,1.4))
pylab.legend()

pylab.subplot(223)
pylab.title(r"15 Hz")
pylab.ylabel(r"$\Delta \omega_{ij} / \omega_{ij}$",fontsize=14)
pylab.xlabel(r"$t^{pre}-t^{post}$ (seconds)",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.axvline(linestyle='--',linewidth=1,color='k')
pylab.hold(True)
execfile('data/theta0.30/pulse_delay_15hz/plot.py')
execfile('data/theta0.33/pulse_delay_15hz/plot.py')
execfile('data/theta0.36/pulse_delay_15hz/plot.py')
pylab.axis((-0.03,0.021,-0.7,1.6))
pylab.legend()

pylab.subplot(224)
pylab.title(r"20 Hz")
pylab.xlabel(r"$t^{pre}-t^{post}$ (seconds)",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.axvline(linestyle='--',linewidth=1,color='k')
pylab.hold(True)
execfile('data/theta0.30/pulse_delay_20hz/plot.py')
execfile('data/theta0.33/pulse_delay_20hz/plot.py')
execfile('data/theta0.36/pulse_delay_20hz/plot.py')
pylab.axis((-0.03,0.021,-0.8,1.8))
pylab.legend()

if save:
  pylab.savefig('stdp_bcm.pdf')
else:
  pylab.show()

