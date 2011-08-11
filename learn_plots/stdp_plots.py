#import numpy
import pylab
import random
import os
import csv
#from matplotlib.ticker import ScalarFormatter, MultipleLocator

debug = True

## Returns a random value from a list of data points
def sample(data):
    for _ in data:
        yield random.choice(data)

## data - list of data points
## func - function to apply to the sampled points (usually numpy.mean)
## n - number of data points to sample from data
## p - confidence interval (e.g. 0.95 for 95% confidence intervals)
## return low,hi tuple
def bootstrapci(data,func,n,p):
    index = int(n*(1-p)/2)
    r = [func(list(sample(data))) for _ in range(n)]
    r.sort()
    return r[index],r[-index]


def make_csv_dict(csv_path,headers=None):
    data = {}
    
    with open(csv_path, 'rb') as f:
        reader = csv.DictReader(f,fieldnames=headers)
        
        for row in reader:
            try:
                for k in row: float(row[k])
            except:
                continue
            for k,v in row.items():
                if data.has_key(k):
                    data[k].append(float(v))
                else:
                    data[k] = [float(v)]
    
    return data


def plot_connection_weight(data,png=False):
    print data.keys()
    if not data.has_key('Time') or not data.has_key('Connection Weight'):
        raise Exception('Passed dictionary must contain "Time" and "Connection Weight" keys.')
    
    figsize = (5,2.5)
    pylab.figure(figsize=figsize,dpi=300)

    pylab.clf()
    pylab.axes((0.15,0.2,0.8,0.7))
    
    pylab.plot(data['Time'],data['Connection Weight'],color='k',linewidth=2)
    #pylab.axhline(baseline,linestyle='--',linewidth=1,color='k')

    pylab.ylabel('Connection Weight\n\n',ha='center')    
    pylab.xlabel('Time (seconds)')
    #pylab.axis('tight')
    
    if png:
        if not os.path.exists('png'):
            os.mkdir('png')
        pylab.savefig('png/connection_weight.png',figsize=figsize,dpi=600)
    else:
        pylab.show()

h = ['Time',
     'Post Stimulation',
     'Pre Stimulation',
     'Post Value',
     'Connection Weight',
     ]

f_pre_post = 'stdp/pre-post.csv'

d = make_csv_dict(f_pre_post,headers=h)
plot_connection_weight(d,False)

"""
def plot_learn_zips_summary(name,control_zip,learn_zips,vals,skip_rows=0,png=False,num_mins=3):
    time_c,control = read_zip(control_zip,skip_rows=skip_rows)
    baseline = 1
    scale = baseline/numpy.mean(control)
    
    figsize = (5,2.5)
    pylab.figure(figsize=figsize,dpi=300)
    
    means = []
    
    for learn_zip in learn_zips:
        time,learn = read_zip(learn_zip,skip_rows=skip_rows)
        means.append(numpy.mean(learn)*scale)
    
    sorted_means = list(means)
    sorted_means.sort()
    min_means_loc = [vals[means.index(sorted_means[i])] for i in range(num_mins)]
    
    ax = pylab.axes((0.18,0.2,0.8,0.7))
    
    fmt = ScalarFormatter()
    fmt.set_powerlimits((-3,4))
    fmt.set_scientific(True)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_locator(MultipleLocator(float(vals[1])-float(vals[0])))
    
    pylab.plot(vals,means,color='k',linewidth=2)
    pylab.plot(min_means_loc,sorted_means[:num_mins],'o',markerfacecolor='None')
    pylab.plot(min_means_loc[0],sorted_means[0],'ko')
    
    pylab.axhline(baseline,linestyle='--',linewidth=1,color='k')
    
    pylab.ylabel('Mean relative error\n(learning vs. analytic)\n\n',ha='center')    
    pylab.xlabel(name)
    pylab.axis('tight')
    
    if png:
        if not os.path.exists('png'):
            os.mkdir('png')
        pylab.savefig('png/'+learn_zips[0].split('-')[0]+'-summary.png',figsize=figsize,dpi=600)
    else:
        pylab.show()

"""
