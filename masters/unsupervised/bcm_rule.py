import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True

theta_1 = 3.0
theta_2 = 2.0
def bcm_rule_1(x):
  return x * (x - theta_1)

def bcm_rule_2(x):
  if x > theta_2:
    return numpy.tanh([(x-theta_2)*2.0])[0]
  return x * (x - theta_2)

x1 = numpy.arange(0.0,5.0,0.1)
x2 = numpy.arange(0.0,5.0,0.1)
y1 = [bcm_rule_1(x) for x in x1]
y2 = [bcm_rule_2(x) for x in x2]

pylab.figure(1,figsize=(8,4))
pylab.subplot(121)
pylab.plot(x1,y1,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.title(r"$y = x (x - \theta)$", fontsize=14)
pylab.axis((0.0,5.0,-2.5,6.0))
pylab.yticks([])
pylab.xticks([theta_1],[r"$\theta$"])

pylab.subplot(122)
pylab.plot(x2,y2,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.title(r"if $x > \theta,$ $y = \tanh (x)$", fontsize=14)
pylab.axis((0.0,5.0,-1.5,1.5))
pylab.yticks([])
pylab.xticks([theta_2],[r"$\theta$"])

if save:
  pylab.savefig('bcm_rule.pdf')
else:
  pylab.show()

