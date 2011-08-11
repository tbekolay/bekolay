import numpy
import pylab
from scipy.ndimage.filters import gaussian_filter1d

from matplotlib import rc

rc('text',usetex=True)
rc('font',family='serif')

my_file = 'data/vStrSpikes.csv'
kim_file = 'data/kim_spikes.csv'

save = True

##################
#Functions called#
##################
def read_file(csv_file):
    z_spikes = None
    
    try:
        f = open(csv_file, 'r')
        rows = f.readlines()
        z_spikes = [[] for _ in range(len(rows))]
        
        for i,row in enumerate(rows):
            if len(row) > 2:
                z_spikes[i] = map(float,row[:-1].split(', '))
        f.close()
    except:
        raise Exception("Error reading %s" % csv_file)
    
    return z_spikes

######
#Data#
######
my_spikes = read_file(my_file)
kim_spikes = read_file(kim_file)

#################
#Data processing#
#################
my_start = 0.6
my_end = 1.1
for i in range(len(my_spikes)):
    my_spikes[i] = filter(lambda t:t >= my_start and t < my_end,my_spikes[i])
    my_spikes[i] = map(lambda t:t-my_start,my_spikes[i])
my_approach = 0.2
my_reward = 0.3
my_delay = 0.4
my_end = 0.5

kim_scale = my_end / max([max(s) for s in kim_spikes])
for i in range(len(kim_spikes)):
    kim_spikes[i] = map(lambda t:t*kim_scale,kim_spikes[i])

bins = 500
x = numpy.linspace(0.0,my_end,num=bins)
bin_size = my_end / bins

sigma = 11.0

kim_bins = [0.0]*bins
for i in range(len(kim_spikes)):
    for s in kim_spikes[i]:
        kim_bins[int(s/bin_size)-1] += 1
kim_filtered = gaussian_filter1d(kim_bins,sigma)

my_bins = [0.0]*bins
for i in range(len(my_spikes)):
    for s in my_spikes[i]:
        my_bins[int(s/bin_size)-1] += 1
my_filtered = gaussian_filter1d(my_bins,sigma)

##########
#Plotting#
##########
pylab.figure(1,figsize=(11,7))
pylab.axes((0.05,0.05,0.9,0.85))
pylab.plot(x,kim_filtered,linewidth=3,color='0.5',label='Experimental')
pylab.plot(x,my_filtered*0.7,linewidth=3,color='k',label='Simulation')
pylab.axvline(my_approach,linestyle='--',linewidth=1,color='k')
pylab.axvline(my_reward,linestyle='--',linewidth=1,color='k')
pylab.axvline(my_delay,linestyle='--',linewidth=1,color='k')
pylab.legend(loc=2)
pylab.title(r"Delay \hspace{10em} Approach \hspace{2.5em} Reward \hspace{3em} Delay",fontsize=20)
pylab.yticks(())
pylab.xticks(())

if save:
  pylab.savefig('filtered_spikes.pdf')
else:
  pylab.show()

