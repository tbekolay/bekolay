import numpy
import pylab

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

##########
#Plotting#
##########
pylab.figure(1,figsize=(6,12))

bottom_axes = (0.10,0.04,0.87,0.445)
top_axes = (bottom_axes[0],bottom_axes[1]+0.47,bottom_axes[2],bottom_axes[3])
pylab.axes(top_axes)
pylab.title(r"Experimental spike trains",fontsize=18)
for i,s in enumerate(kim_spikes):
    pylab.plot(s,[i]*len(s),linestyle='None',markerfacecolor='0.3',marker='o',markersize=5.0)
pylab.axvline(my_approach,linestyle='--',linewidth=1,color='k')
pylab.axvline(my_reward,linestyle='--',linewidth=1,color='k')
pylab.axvline(my_delay,linestyle='--',linewidth=1,color='k')
pylab.ylabel(r"Trial number")
pylab.xticks(())
pylab.text(0.06,-2.25,r"Delay \hspace{2.7em} Approach~~Reward~~Delay",fontsize=18)

pylab.axes(bottom_axes)
for i,s in enumerate(my_spikes):
    pylab.plot(s,[i]*len(s),linestyle='None',markerfacecolor='0.3',marker='o',markersize=5.0)
pylab.axvline(my_approach,linestyle='--',linewidth=1,color='k')
pylab.axvline(my_reward,linestyle='--',linewidth=1,color='k')
pylab.axvline(my_delay,linestyle='--',linewidth=1,color='k')
pylab.ylabel(r"Neuron number")
pylab.xticks(())
pylab.xlabel(r"Simulated spike trains",fontsize=18)

if save:
  pylab.savefig('spikes.pdf')
else:
  pylab.show()

