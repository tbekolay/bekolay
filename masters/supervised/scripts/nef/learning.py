import plasticity
import numeric
import datetime
import os
import sys
from copy import copy

sharcnet = False
testing = False
view = False
if not sharcnet:
    param = 'oja'

## Set of possible functions to learn
def mult(x):
    return [x[0]*x[1]]

def mult_combine(x):
    return [x[0]*x[1] + x[2]*x[3]]

def mult_3(x):
    return [x[0]*x[1],x[0]*x[2],x[1]*x[2]]

def cconv_2(x):
    return numeric.circconv([x[0],x[1]],[x[2],x[3]])

def cconv_3(x):
    return numeric.circconv([x[0],x[1],x[2]],[x[3],x[4],x[5]])

def channel(x):
    return x

def square(x):
    return [x[0]*x[0]]
##

static_params = {'func': mult_combine,
                 'in_dim': 4,
                 'out_dim': 1,
                 'train_len': 2.5,
                 'stdp': False,
                 'rate': 1e-7,
                 'NperD': 84,
                 'length': 100.0,
                 'decay': None,
                 'homeostasis': None,
                 'oja':False,
                 'directory': 'trevor/learning/',
                 'learning': True}
func_name = 'X1X2'

if sharcnet:
    ca.nengo.util.impl.NodeThreadPool.setNumThreads(0)

if view:
    static_params['directory'] = None
    net = plasticity.run_experiment(name='Learn'+func_name,**static_params)
    net.view()
else:
    if param == 'all_tau' or param.startswith('t'):
        lowest_val = 1.0
        step = 10.0
    elif param.startswith('a'): # also captures 'all_a'
        lowest_val = 0.0
        step = 5e-4
    elif param == 'decay':
        lowest_val = 0.0
        step = 5e-9
    elif param == 'homeostasis':
        lowest_val = 5.0e-3
        step = 5.0e-3
    else:
        # test oja
        num_tests = 40
        for i in range(num_tests):
            params = copy(static_params)
            params['oja'] = False
            net = plasticity.run_experiment(name=func_name,**params)
        sys.exit()
    
    if testing:
        tests_per_val = 2
        num_vals = 2
    else:
        tests_per_val = 20
        num_vals = 10
    
    vals = ['%#.2e'%(lowest_val+i*step) for i in range(num_vals)]
    
    # Write things to disk
    now = datetime.datetime.now()
    param_file_name = param+'-'+func_name+'-'+now.strftime("%Y-%m-%d_%H-%M-%S")+'-params.txt'
    param_path = os.path.join(static_params['directory'],param_file_name)
    plot_path = os.path.join(static_params['directory'],'plot_'+param+'-'+func_name+'-'+now.strftime("%Y-%m-%d_%H-%M-%S")+'.py')
    
    def write_param_info():
        f = open(param_path, 'w')
        f.write('Parameters:\nname = %s\n' % param)
        for k,v in static_params.items():
            f.write("%s = %s\n" % (k,str(v)))
        f.write('Varying %s\n' % param)
        f.write('%s\n' % str(vals))
        f.close()
    
    def make_plot_py():
        f = open(plot_path, 'w')
        f.write("""import sys
sys.path.append('/home/tbekolay/Dropbox/Programming/trevor_misc/python')
import learning_plots
control_zip = 'Control%(func_name)s_%(NperD)dN.zip'
param_file = '%(param_file_name)s'
params = learning_plots.read_params(param_file)
if not params.has_key('name') or not params.has_key('vals'):
    raise Exception('Error in param file, %%s' %% param_file)
learn_zips = [params['name']+'-%(func_name)s-'+val+'.zip' for val in params['vals']]
learning_plots.plot_learn_zips(control_zip,learn_zips,name=params['name'],vals=params['vals'],skip_rows=0,png=True)""" \
        % {'func_name':func_name, 'param_file_name':param_file_name, 'NperD':static_params['NperD']})
    
    write_param_info()
    make_plot_py()
    
    val = lowest_val-step
    for i in range(tests_per_val*num_vals):
        if i % tests_per_val == 0:
            val += step
        
        params = copy(static_params)
        
        if param == 'all_a':
            params['a2Minus'] = val
            params['a3Minus'] = val
            params['a2Plus'] = val
            params['a3Plus'] = val
        elif param == 'all_tau':
            params['tauMinus'] = val
            params['tauPlus'] = val
            params['tauX'] = val
            params['tauY'] = val
        else:
            params[param] = val
        
        net = plasticity.run_experiment(name=param+'-'+func_name+'-'+'%#.2e'%val,**params)
        net.network = None # dunno if this'll help with garbage collection, but hopefully

