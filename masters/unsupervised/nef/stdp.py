import random

import sys
import nef
import datetime
import os

directory = 'trevor/stdp-bcm' # set to a directory to run an experiment
vary = 'pulse_delay'
dt = 0.0005
min_weight = 5e-4
max_weight = 2e-3

class ExperimentRunner(nef.SimpleNode):
    def __init__(self,name,pulse_rate=1.0,pulse_delay=-0.02,pulse_dur=0.003,pulse_height=1.0,dt=dt):
        """
        pulse_rate: frequency of pulse, in Hz
        pulse_delay: delay between pre and post pulses, in seconds
        pulse_dur: length of pulse, in seconds
        
        """
        
        self.dt = dt
        self.pulse_rate = pulse_rate
        self.pulse_gap = 1.0 / pulse_rate
        self.pulse_delay = pulse_delay
        self.pulse_steps = int(round(pulse_dur / dt))
        self.pulse_height = pulse_height
        
        self.last_pre_pulse = 0.0
        self.last_post_pulse = self.pulse_delay
        self.steps_since_pre = 0
        self.steps_since_post = 0
        
        self.post_x_average = 0.33
        # 10 minutes = 600 seconds / dt = 1200000
        self.history_len = int(600 / dt)
        self.post_x = [self.post_x_average]*self.history_len
        
        self.data_log = []
        
        nef.SimpleNode.__init__(self,name)
    
    def origin_stim_pre(self):
        if self.t_start >= self.last_pre_pulse+self.pulse_gap and \
           self.steps_since_pre < self.pulse_steps:
            self.steps_since_pre += 1
            return [self.pulse_height]
        elif self.steps_since_pre == self.pulse_steps:
            self.last_pre_pulse = self.t_start-(self.pulse_steps*self.dt)
            self.steps_since_pre = 0
            return [0.0]
        else:
            return [0.0]
    
    def origin_stim_post(self):
        if self.t_start >= self.last_post_pulse+self.pulse_gap and \
           self.steps_since_post < self.pulse_steps:
            self.steps_since_post += 1
            return [self.pulse_height]
        elif self.steps_since_post == self.pulse_steps:
            self.last_post_pulse = self.t_start-(self.pulse_steps*self.dt)
            self.steps_since_post = 0
            return [0.0]
        else:
            return [0.0]
        
    def origin_bcm(self):
        scale = 5.0
        bcm_thresh = self.post_x_average
        self.data_log.append('thresh=%f\ty=%f\tbrackets=%f\tbcm=%f'%(bcm_thresh,self.post_x[0],self.post_x[0]-bcm_thresh,
                                                                     self.post_x[0] * (self.post_x[0]-bcm_thresh)))
        return [self.post_x[0] * (self.post_x[0]-bcm_thresh) * scale] # / bcm_thresh
    
    def termination_post(self,x):
        last_x = self.post_x.pop()
        self.post_x_average -= last_x**2 / self.history_len
        self.post_x_average += x**2 / self.history_len
        self.post_x.insert(0,x)
    
    def write_data_log(self, filename):
        """Attempts to write the contents of self.data_log to
        the file pointed to by the consumed string, filename.
        If there is an error writing to that file,
        the contents of self.data_log are printed to console instead.
        """
        try:
            f = open(filename, 'w')
        except:
            print "Error opening %s" % filename
            return self.print_data_log()
        
        for line in self.data_log:
            f.write("%s\n" % line)
        f.close()
    
    def print_data_log(self):
        """Prints the contents of self.data_log to the console."""
        for line in self.data_log:
            print line

def rand_weights(w):
    for i in xrange(len(w)):
        for j in xrange(len(w[0])):
            w[i][j] = random.uniform(min_weight,max_weight) # keep positive
    return w

def create_network(**kwargs):
    net = nef.Network('STDP Experiment')
    
    experiment = ExperimentRunner('ExperimentRunner',**kwargs)
    net.add(experiment)
    experiment.getTermination('post').setTau(0.015)
    
    pre = net.make('pre',1,1,max_rate=[100],intercept=[0.0],encoders=[[1.0]])
    net.connect(experiment.getOrigin('stim_pre'),pre)
    
    post = net.make('post',1,1,max_rate=[100],intercept=[0.0],encoders=[[1.0]])
    net.connect(experiment.getOrigin('stim_post'),post)
    
    net.connect(pre,post,weight_func=rand_weights)
    
    learn_args = {'stdp':False, 'rate':1e-4, 'oja':False}
    net.connect(post,experiment.getTermination('post'))
    net.connect(experiment.getOrigin('bcm'),post,modulatory=True)
    net.learn(post,'pre','bcm',**learn_args)
    
    return net

def run_experiment(**kwargs):
    # An experiment is: take the connection weight beforehand, run
    # the network for 4 seconds, and take the connection weight afterward.
    # Repeat 20 times to get a good confidence interval.
    
    data_log = []
    
    for i in range(20):
        net = create_network(**kwargs)
        net.network.setStepSize(dt)
        post = net.network.getNode('post')
        term = post.getTermination('pre')
        before_weight = term.getTransform()[0][0]
        net.network.run(0,3.0)
        after_weight = term.getTransform()[0][0]
        if after_weight < min_weight: after_weight = min_weight
        if after_weight > max_weight: after_weight = max_weight
        change = (after_weight - before_weight) / before_weight
        data_log.append(str(before_weight)+', '+str(after_weight)+', '+str(change))
    
    return data_log

if directory != None:
    vals = None
    if vary == 'pulse_rate':
        vals = [0.1,1.0,5.0,10.0,20.0,50.0,100.0]
    elif vary == 'pulse_delay':
        vals = [n*0.001 for n in range(-30,21,1)]
    
    if vals is not None:
        for val in vals:
            log = run_experiment(**dict({vary: val}))
            
            if val < 0.0: sign = ''
            else: sign = '+'
            
            f_name = os.path.join(directory, vary+sign+str(val)+'.csv')
            try:
                f = open(f_name, 'w')
            except:
                print "Error opening %s" % f_name
                break
    
            for line in log:
                f.write("%s\n" % line)
            f.close()

else:
    net = create_network()
    net.view()
