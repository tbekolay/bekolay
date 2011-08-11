import math
import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True
use_sub = True

pylab.figure(1,figsize=(12,5))
pylab.subplot(131)
pylab.title(r"Pre 20ms before post")
pylab.ylabel(r"$\Delta \omega_{ij} / \omega_{ij}$",fontsize=14)
pylab.xlabel(r"Spike frequency (hz)",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.gca().set_xscale('log')
pylab.hold(True)
execfile('data/theta0.30/pulse_rate_post_pre/plot.py')
execfile('data/theta0.33/pulse_rate_post_pre/plot.py')
execfile('data/theta0.36/pulse_rate_post_pre/plot.py')
pylab.axis((0.07,110.0,-0.6,1.8))
pylab.legend(loc=2)

pylab.subplot(132)
pylab.title(r"Pre same time as post")
pylab.xlabel(r"Spike frequency (hz)",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.gca().set_xscale('log')
pylab.hold(True)
execfile('data/theta0.30/pulse_rate_same/plot.py')
execfile('data/theta0.33/pulse_rate_same/plot.py')
execfile('data/theta0.36/pulse_rate_same/plot.py')
pylab.axis((0.07,110.0,-0.6,1.8))
pylab.legend(loc=2)

pylab.subplot(133)
pylab.title(r"Post 20ms before pre")
pylab.xlabel(r"Spike frequency (hz)",fontsize=14)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.gca().set_xscale('log')
pylab.hold(True)
execfile('data/theta0.30/pulse_rate_pre_post/plot.py')
execfile('data/theta0.33/pulse_rate_pre_post/plot.py')
execfile('data/theta0.36/pulse_rate_pre_post/plot.py')
pylab.axis((0.07,110.0,-0.6,1.8))
pylab.legend(loc=2)

if save:
  pylab.savefig('stdp_bcm_freq_dependence.pdf')
else:
  pylab.show()

