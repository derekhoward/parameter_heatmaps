# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:16:42 2015

@author: derek
"""

import numpy as np
import matplotlib.pyplot as plt
import neuron

def make_compartment(length=25, diameter=25, nseg=1, name="soma"):
  """
  Returns a compartment.

    comp = make_compartment(25, 25) # comp.L: 25 comp.diam: 25; comp.nsg: 1
    comp = make_compartment()       # comp.L: 25; comp.diam: 25; comp.nsg: 1
  """
  compartment = neuron.h.Section(name=name)
  compartment.L = length
  compartment.diam = diameter
  compartment.nseg = nseg
  return compartment
  
class Neuron(object):
    def __init__(self):
    # creating compartments
        self.soma = make_compartment(25, 25, 1, "soma")
        #self.neuron.h.finitialize
        self.insert_mechanisms()
    
    def insert_mechanisms(self):
        for sec in neuron.h.allsec():
            sec.insert("HT")
            sec.insert("LT")
            sec.insert("NaCh")
            sec.insert("nap")
            
    def set_conductances(self, **kwargs):
        """
        Expects keyword arguments of the format
        <section-name>_<mechname> which supply
        the value of the conductances for each mechanism
        """
        for name, value in kwargs.iteritems():
            secname, mechname = name.split('_')
            sec = getattr(self, secname)
            mech = getattr(sec(0.5), mechname)
            mech.gbar = value    
    
class Simulation(object):
    def __init__(self, cell, delay=1, amp=1, dur=3, sim_time=200, dt=0.025):
        self.cell = cell
        self.sim_time = sim_time
        self.dt = dt
    
    
    def set_IClamp(self, delay=5, amp=0.5, dur=100):
        """
        Initializes Iclamp values
        """
        stim = neuron.h.IClamp(self.cell.soma(0.5))
        stim.delay = delay
        stim.amp = amp
        stim.dur = dur
        self.stim = stim

    def set_recording(self):
        # Record Time
        self.rec_t = neuron.h.Vector()
        self.rec_t.record(neuron.h._ref_t)
        # Record Voltage
        self.rec_v = neuron.h.Vector()
        self.rec_v.record(self.cell.soma(0.5)._ref_v)

    def get_recording(self):
        time = np.array(self.rec_t)
        voltage = np.array(self.rec_v)
        return time, voltage    
        
        
    def go(self, sim_time=None):
        self.set_recording()
        self.set_IClamp()
        neuron.h.dt = self.dt
        neuron.h.finitialize(-70)
        neuron.init()
        if sim_time:
            neuron.run(sim_time)
        else:
            neuron.run(self.sim_time)
        self.go_already = True
        
    def show(self):
        if self.go_already:
            x = np.array(self.rec_t)
            y = np.array(self.rec_v)
            plt.plot(x, y)
            plt.title("")
            plt.xlabel("Time [ms]")
            plt.ylabel("Voltage [mV]")
            #plt.axis(ymin=-120, ymax=-50)
        else:
            print("""First you have to `go()` the simulation.""")
        plt.show()
        
cell=Neuron()
"""
cell.set_conductances(soma_NaCh=0.03) #0.05
cell.set_conductances(soma_nap=5e-05) #0.0005
cell.set_conductances(soma_HT=0.08) #0.015
cell.set_conductances(soma_LT=0.01) #0.002
"""
cell.set_conductances(soma_NaCh=0.05) #
cell.set_conductances(soma_nap=0) #
cell.set_conductances(soma_HT=0.015) #0.015
cell.set_conductances(soma_LT=0.002) #0.002
sim=Simulation(cell)
sim.go()  

import efel
time, voltage= sim.get_recording()
trace = {}
trace['T'] = time
trace['V'] = voltage
trace['stim_start'] = [5]
trace['stim_end'] = [105]
traces = [trace]

features = efel.getFeatureValues(traces, ["AP1_width", "Spikecount"])
#voltage_base = features[0]["voltage_base"][0]
first_width = features[0]["AP1_width"][0]
spikecount = features[0]["Spikecount"][0]


sim.show()
