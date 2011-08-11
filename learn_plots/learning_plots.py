import numpy
import random
import zipfile
import pylab
import os
from matplotlib.ticker import ScalarFormatter, MultipleLocator

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

## Takes in a zip file and returns a tuple with
##  - time axis
##  - sum of all data columns
def read_zip(zip_path,skip_rows=0):
    z_time = None
    z_data = None
    
    try:
        zf = zipfile.ZipFile(zip_path, 'r')
        for f in zf.namelist():
            csv_f = zf.open(f)
            rows = csv_f.readlines()
            
            if not z_time:
                z_time = [[] for _ in range(len(rows)-skip_rows)]
                z_data = [[] for _ in range(len(rows)-skip_rows)]
            
            for ix,row in enumerate(rows):
                if ix >= skip_rows:
                    row_l = row[:-1].split(', ')
                    z_time[ix-skip_rows] = float(row_l[0])
                    z_data[ix-skip_rows].append(sum(map(float,row_l[1:])))
        zf.close()
    except:
        raise Exception("Error reading %s" % zip_path)
    
    return (z_time,z_data)

def plot_learn_zips(control_zip,learn_zips,name=None,vals=None,skip_rows=0,png=False):
    for learn_zip in learn_zips:
        plot_learn_zip(control_zip,learn_zip,skip_rows=skip_rows,png=png)
    
    if name and vals:
        plot_learn_zips_summary(name,control_zip,learn_zips,vals,skip_rows=skip_rows,png=png)

def plot_learn_zip(control_zip,learn_zip,skip_rows=0,png=False):
    _,control = read_zip(control_zip,skip_rows=skip_rows)
    
    baseline = 1
    scale = baseline/numpy.mean(control)
    
    figsize = (5,2.5)
    pylab.figure(figsize=figsize,dpi=300)
    
    time,learn = read_zip(learn_zip,skip_rows=skip_rows)

    mean = []
    cil = []
    cih = []
    for x in learn:
        x= [y*scale for y in x]
        mean.append(numpy.mean(x))
        l,h = bootstrapci(x,numpy.mean,1000,0.95)
        cil.append(l)
        cih.append(h)

    pylab.clf()
    pylab.axes((0.15,0.2,0.8,0.7))
    
    pylab.fill_between(time,y1=cil,y2=cih,color='0.8')
    pylab.plot(time,mean,color='k',linewidth=2)

    pylab.axhline(baseline,linestyle='--',linewidth=1,color='k')
    
    pylab.ylabel('Relative error\n(learning vs. analytic)\n\n',ha='center')    
    pylab.xlabel('Learning time (seconds)')
    pylab.axis([time[0], time[-1], 0.95, 2.0])
    
    if png:
        if not os.path.exists('png'):
            os.mkdir('png')
        pylab.savefig('png/'+learn_zip[:-3]+'png',figsize=figsize,dpi=600)
    else:
        pylab.show()

def plot_learn_zips_summary(name,control_zip,learn_zips,vals,skip_rows=0,png=False,num_mins=3):
    _,control = read_zip(control_zip,skip_rows=skip_rows)
    baseline = 1
    scale = baseline/numpy.mean(control)
    
    figsize = (5,2.5)
    pylab.figure(figsize=figsize,dpi=300)
    
    means = []
    
    for learn_zip in learn_zips:
        _,learn = read_zip(learn_zip,skip_rows=skip_rows)
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

## Takes in a param file, outputs a dictionary with the parameters read in.
def read_params(f_name):
    params = {}
    
    with open(f_name,'r') as f:
        l = f.readline()
        # First line is just "Parameters:"
        
        # Next block are the parameters
        l = f.readline()
        
        while 'Varying' not in l:
            l_s = l.split()
            # ['param', '=', 'val']
            params[l_s[0]] = ' '.join(l_s[2:])
            
            l = f.readline()
        
        # Can get varied param here... 'Varying %s'
        
        l = f.readline()
        # Next is the list of possible varied values.

        params['vals'] = filter(lambda x: x != "'", l[1:-2]).split(', ')
    
    return params

## Takes in a set of parameters stored in a dictionary, and a directory in which to
## search. Zips together any CSV files that match the parameter sweep indicated by
## the param deictionary.
def zip_files_from_params(params, directory, func_name=None):
    d_files = os.listdir(directory)
    
    if not params.has_key('vals') or not params.has_key('name'):
        raise Exception('params must have "vals" and "name" keys.')
    
    vals = params['vals']
    
    for val in vals:
        if func_name is not None:
            zip_path = directory+params['name']+'-'+func_name+'-'+val+'.zip'
        else:
            zip_path = directory+params['name']+'-'+val+'.zip'
        if debug:
            print "Creating "+zip_path+' ...'
        newzip = zipfile.ZipFile(zip_path, 'a')
        
        for f in d_files:
            if (func_name is not None and f.startswith(params['name']+'-'+func_name+'-'+val) and
                    f.endswith('.csv')) or (f.startswith(params['name']+'-'+val) and f.endswith('.csv')):
                f_path = directory+f
                if debug:
                    print "\tAdding and deleting "+f
                newzip.write(f_path,arcname=f)
                os.remove(f_path)
        
        newzip.close()
        if os.path.getsize(zip_path) == 0:
            if debug:
                print "Empty zip. Deleting "+zip_path+' ...'
            os.remove(zip_path)
        d_files = os.listdir(directory)

## Finds all the param files in a directory and calls
## zip_files_from_params for each of them.
def zip_all(directory):
    files = os.listdir(directory)
    
    for f in files:
        if 'params' in f:
            if debug:
                print "Parsing "+f+"..."
            
            func_name = None
            if f.split('-')[1][:-2].isalpha():
                func_name = f.split('-')[1]
            
            f_path = directory+f
            params = read_params(f_path)
            zip_files_from_params(params,directory,func_name)
