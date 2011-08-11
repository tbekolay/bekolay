import numpy
import pylab

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

save = True

in_dims = [2, 4, 3, 4, 6]
out_dims = [1, 1, 3, 2, 3]
dims = [in_dims[i]+out_dims[i] for i in range(len(in_dims))]
learn_time = [37.5, 65.24, 65.4, 43.6, 90.0] # the time at which the 95% confidence interval hits 1.0

order = 1

l_in = numpy.polyfit(in_dims,learn_time,order)
p_in = numpy.poly1d(l_in)
l_out = numpy.polyfit(out_dims,learn_time,order)
p_out = numpy.poly1d(l_out)
l_all = numpy.polyfit(dims,learn_time,order)
p_all = numpy.poly1d(l_all)

x1 = numpy.arange(1.0,7.0,0.1)
y1 = p_in(x1)
x2 = numpy.arange(0.5,3.5,0.1)
y2 = p_out(x2)
x3 = numpy.arange(2.0,10.0,0.1)
y3 = p_all(x3)
print p_all(1000)

pylab.figure(1,figsize=(11,5))
pylab.subplot(131)
pylab.scatter(in_dims,learn_time,color='k')
pylab.plot(x1,y1,linestyle='--',linewidth=1,color='k')
pylab.ylabel(r"Time to learn")
pylab.xlabel(r"Input dimensions")

pylab.subplot(132)
pylab.scatter(out_dims,learn_time,color='k')
pylab.plot(x2,y2,linestyle='--',linewidth=1,color='k')
pylab.xlabel(r"Output dimensions")

pylab.subplot(133)
pylab.scatter(dims,learn_time,color='k')
pylab.plot(x3,y3,linestyle='--',linewidth=1,color='k')
pylab.xlabel(r"Input+Output dimensions")

if save:
  pylab.savefig('time_to_learn.pdf')
else:
  pylab.show()

