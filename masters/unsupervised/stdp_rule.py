import math
import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = False

a_minus = -1.0
tau_minus = 0.02
a_plus = 1.0
tau_plus = 0.01

def stdp_rule(x):
  if x < 0.0:
    return a_minus * math.exp(x / tau_minus)
  else:
    return a_plus * math.exp(-x / tau_plus)

x = numpy.arange(-0.05,0.05,0.001)
y = [stdp_rule(xx) for xx in x]

pylab.figure(1,figsize=(6,3))
#pylab.axes((0.1,0.2,0.85,0.7))
pylab.plot(x,y,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
#pylab.axis([0.0,2.5,-1.5,1.5])
#pylab.yticks((delta_minus,delta_plus),(r"$\Delta^{-}$",r"$\Delta^{+}$"))
#pylab.xticks((theta_minus,theta_plus),(r"$\theta^{-}$",r"$\theta^{+}$"))

if save:
  pylab.savefig('stdp_rule.pdf')
else:
  pylab.show()

