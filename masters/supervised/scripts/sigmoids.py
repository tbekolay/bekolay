import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True

def sig1(x):
  return numpy.tanh([x])[0]

def sig2(x):
  return 1.0 / (1.0 + numpy.exp([-x])[0])

x1 = numpy.arange(-3.0,3.0,0.1)
x2 = numpy.arange(-6.0,6.0,0.1)
y1 = [sig1(x) for x in x1]
y2 = [sig2(x) for x in x2]

pylab.figure(1,figsize=(8,4))
pylab.subplot(121)
pylab.plot(x1,y1,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.title(r"$y = \tanh (x)$", fontsize=16)

pylab.subplot(122)
pylab.plot(x2,y2,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.title(r"$y = \frac{1}{1 + e^{-x}}$", fontsize=16)

if save:
  pylab.savefig('sigmoids.pdf')
else:
  pylab.show()

