import plasticity
import numeric
import datetime
import os
from copy import copy

sharcnet = False
testing = False

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

static_params = {'func': mult_3,
                 'in_dim': 3,
                 'out_dim': 3,
                 'train_len': 4.0,
                 'NperD': 84,
                 'length': 100.0,
                 'directory': 'trevor/learning/',
                 'learning': False}
func_name = 'Mult3'

if sharcnet:
    ca.nengo.util.impl.NodeThreadPool.setNumThreads(0)

if testing:
    tests = 2
else:
    tests = 50

for i in range(tests):
    net = plasticity.run_experiment(name='Control'+func_name+'_'+'%dN'%static_params['NperD'],**static_params)
    net.network = None

