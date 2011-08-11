import random
import scipy.io
import numpy
import pylab

from matplotlib import rc

use_sub = True
save = False

rc('text',usetex=True)
rc('font',family='serif')

figsize = (12,8)
f = pylab.figure(figsize=figsize)
execfile('mult.py')
execfile('x1x2.py')
execfile('x1x2x3.py')
execfile('2dconv.py')
execfile('3dconv.py')

if save:
    pylab.savefig('all_funcs.pdf')
else:
    pylab.show()
