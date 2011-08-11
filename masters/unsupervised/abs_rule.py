import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True

theta_minus = 0.5
delta_minus = -1.0
theta_plus = 1.5
delta_plus = 1.0

def abs_rule(x):
  if x > theta_plus:
    return delta_plus
  elif x > theta_minus:
    return delta_minus
  return 0.0

x = numpy.arange(0.0,2.5,0.001)
y = [abs_rule(xx) for xx in x]

pylab.figure(1,figsize=(4,1.5))
pylab.axes((0.1,0.2,0.85,0.7))
pylab.plot(x,y,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.axis([0.0,2.5,-1.5,1.5])
pylab.yticks((delta_minus,delta_plus),(r"$\Delta^{-}$",r"$\Delta^{+}$"))
pylab.xticks((theta_minus,theta_plus),(r"$\theta^{-}$",r"$\theta^{+}$"))

if save:
  pylab.savefig('abs_rule.pdf')
else:
  pylab.show()

