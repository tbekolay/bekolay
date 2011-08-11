import random
import scipy.io
import numpy
import pylab
import zipfile

from matplotlib import rc

try:
    use_sub
except NameError:
    use_sub = False

try:
    save
except NameError:
    save = False

rc('text',usetex=True)
rc('font',family='serif')

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
def sample(data):
    for _ in data:
        yield random.choice(data)
def bootstrapci(data,func,n,p):
    index = int(n*(1-p)/2)
    r = [func(list(sample(data))) for _ in range(n)]
    r.sort()
    return r[index],r[-index]

###################
# Data processing #
###################
_,control = read_zip('data/ControlX1X2_84N.zip')
time,learn = read_zip('data/x1x2.zip')
baseline = 1
scale = baseline/numpy.mean(control)
mean = []
cil = []
cih = []
for x in learn:
    x= [y*scale for y in x]
    mean.append(numpy.mean(x))
    l,h = bootstrapci(x,numpy.mean,1000,0.95)
    cil.append(l)
    cih.append(h)

############
# Plotting #
############
figsize = (8,8)
if not use_sub:
    pylab.figure(figsize=figsize)
else:
    #[left, bottom, width, height]
    h_pad = 0.03
    bottom_pad = 0.02
    v_pad = bottom_pad+0.05
    pylab.axes([0.33+h_pad, 0.5+bottom_pad, 0.33-h_pad, 0.5-v_pad])

pylab.fill_between(time,y1=cil,y2=cih,color='0.8')
pylab.plot(time,mean,color='k',linewidth=2)
pylab.axhline(baseline,linestyle='--',linewidth=1,color='k')
#pylab.axis([xmin, xmax, ymin, ymax])
pylab.axis([0.0, 100.0, 0.8, 2.4])

if not use_sub:
    pylab.ylabel(r"Relative error (learning vs. analytic)",ha='center')    
if not use_sub:
    pylab.xlabel(r"Learning time (seconds)")
pylab.title(r"$f(\mathbf{x}) = x_1 x_2 + x_3 x_4$",fontsize=16)

if save and not use_sub:
    pylab.savefig('x1x2.pdf')
if not save and not use_sub:
    pylab.show()
