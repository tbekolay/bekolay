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
data = scipy.io.loadmat('data/3dconv.mat',struct_as_record=False)
learn = data['l_data']
control_old = data['n_data']

_,control_new = read_zip('data/Control3DConv_67N.zip')

time = data['time'].T[0]
baseline = 1
scale = baseline/numpy.mean(control_old)
baseline_new = scale*numpy.mean(control_new)
mean = []
cil = []
cih = []
for x in learn:
    x = x*scale
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
    bottom_pad = 0.06
    v_pad = bottom_pad+0.05
    pylab.axes([0.6, 0.0+bottom_pad, 0.33, 0.5-v_pad])

pylab.fill_between(time,y1=cil,y2=cih,color='0.8')
pylab.plot(time,mean,color='k',linewidth=2)
pylab.axhline(baseline,linestyle='--',linewidth=1,color='k')
pylab.axhline(baseline_new,linestyle='--',linewidth=1,color='k')
if use_sub:
    pylab.text(10.0,baseline+0.01,"3 layer control",figure=f,fontsize=12)
    pylab.text(300.0,baseline_new+0.01,"2 layer control",figure=f,fontsize=12)
#pylab.axis([xmin, xmax, ymin, ymax])
pylab.axis([0.0, 400.0, 0.9, 2.3])

if not use_sub:
    pylab.ylabel(r"Relative error (learning vs. analytic)",ha='center')    
pylab.xlabel(r"Learning time (seconds)")
pylab.title(r"$f(\mathbf{x}) = \left[x_1,x_2,x_3\right] \otimes \left[x_4,x_5,x_6\right]$",fontsize=16)

if save and not use_sub:
    pylab.savefig('3dconv.pdf')
if not save and not use_sub:
    pylab.show()
