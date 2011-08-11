import numpy
import pylab

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True

theta_minus = 0.5
theta_plus = 2.5

def abs_rule(x):
  if x < theta_minus:
    return 0.0
  elif x > theta_plus:
    return numpy.tanh([(x-theta_plus)*2.0])[0]
  return (x - theta_minus) * (x - theta_plus)

def abs_rule_3d(x,y):
  t_minus = theta_minus-y
  t_plus = theta_plus-y
  if x < t_minus:
    return 0.0
  elif x > t_plus:
    return numpy.tanh([(x-t_plus)*2.0])[0]
  return (x - t_minus) * (x - t_plus)

x = numpy.arange(0.0,5.0,0.01)
y = [abs_rule(xx) for xx in x]

################
# First subplot
################
f = pylab.figure(figsize=(8,4))
pylab.axes((0.04,0.08,0.44,0.89))
pylab.plot(x,y,color='k',linewidth=2)
pylab.axhline(linestyle='--',linewidth=1,color='k')
pylab.axis([0.0,5.0,-1.5,1.5])
pylab.yticks((-0.5,0.5),(r"$\ominus$",r"$\oplus$"))
pylab.xticks((theta_minus,theta_plus),(r"$\theta^{-}$",r"$\theta^{+}$"))

#################
# Second subplot
#################

ax = Axes3D(f,[0.5,0.0,0.5,1.0])
X = numpy.arange(0.0, 4.0, 0.05)
Y = numpy.arange(-2.0, 2.0, 0.05)
X,Y = numpy.meshgrid(X, Y)
v_abs = numpy.vectorize(abs_rule_3d)
Z = v_abs(X,Y)
ax.plot_surface(X, Y, Z)

if save:
  pylab.savefig('abs_rule_2.png',dpi=600)
else:
  pylab.show()

