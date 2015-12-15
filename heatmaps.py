# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 17:43:46 2015

@author: derek
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import conductancemodel
import efel

cell = conductancemodel.Neuron()
"""
cell.set_conductances(soma_NaCh=0.03) #0.05
cell.set_conductances(soma_nap=5e-05) #0.0005
cell.set_conductances(soma_HT=0.08) #0.015
cell.set_conductances(soma_LT=0.01) #0.002
"""
cell.set_conductances(soma_NaCh=0.05) #
cell.set_conductances(soma_nap=0) #()5e-05
#cell.set_conductances(soma_HT=0.015) #0.015
cell.set_conductances(soma_LT=0.002) #0.002




ht_range = np.arange(0.008, 0.03, 0.001)

#nap_range = np.arange(0.000001, 0.000007, 0.000001)
#lt_range = np.arange(0.0015, 0.004, 0.0001)
#nach_range = np.arange(0.04, 0.07, 0.01)
nach_range = np.arange(0.04, 0.07, 0.005)

first_width = []
second_width = []
spikecount = []

def plot_heatmap(df, title, xlabel, ylabel, save=False, output_filename='plot.png'):
    fig, ax = plt.subplots()
    fig.set_figheight(12)
    fig.set_figwidth(14)
    sns.heatmap(df, annot=True, cmap="YlOrRd_r", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if save == True:
        plt.savefig(output_filename)

for ht_conductance in ht_range:
    temp_width = []
    temp_width2 = []
    temp_spikecount= []
    cell.set_conductances(soma_HT=ht_conductance)
    
    for nach_conductance in nach_range:
        cell.set_conductances(soma_NaCh=nach_conductance)
        sim = conductancemodel.Simulation(cell)
        sim.go()  
        time, voltage = sim.get_recording()
        trace = {}
        trace['T'] = time
        trace['V'] = voltage
        trace['stim_start'] = [5]
        trace['stim_end'] = [105]
        traces = [trace]
        features = efel.getFeatureValues(traces, ["AP1_width", "AP2_width", "Spikecount", "trace_check"])
        #voltage_base = features[0]["voltage_base"][0]
        #first_width = first_width.append(features[0]["AP1_width"][0])
        #spikecount = spikecount.append(features[0]["Spikecount"][0])
        
#this should probably not output a width of 0, but a NaN value        
        if features[0]["AP1_width"].size == 0:
            temp_width.append(np.nan)
        elif features[0]["AP1_width"] > 3:
            temp_width.append(np.nan)        
        else:
            temp_width.append(features[0]["AP1_width"][0])
            
        if features[0]["AP2_width"].size == 0:
            temp_width2.append(np.nan)
        elif features[0]["AP2_width"] > 3:
            temp_width2.append(np.nan)        
        else:
            temp_width2.append(features[0]["AP2_width"][0])
        
        if features[0]["trace_check"] is None:
            temp_spikecount.append(np.nan)
        elif features[0]["Spikecount"].size == 0:
            temp_spikecount.append(np.int64(0))
        else:
            temp_spikecount.append(features[0]["Spikecount"][0])
            
        
        #sim.show()
        #print("KHT:", ht_conductance, "Nap:", nach_conductance, features)
    first_width.append(temp_width)
    second_width.append(temp_width2)
    spikecount.append(temp_spikecount)
    

df1=pd.DataFrame(first_width)
df2=pd.DataFrame(second_width)
df3=pd.DataFrame(spikecount)

df1.index = ht_range
df1.index.name = 'HT K+'
df1 = df1.reindex(index=df1.index[::-1])
df1.columns = nach_range
df1.columns.name = 'Transient Na+'

df2.index = ht_range
df2.index.name = 'HT K+'
df2 = df2.reindex(index=df2.index[::-1])
df2.columns = nach_range
df2.columns.name = 'Transient Na+'

df3.index = ht_range
df3.index.name = 'HT K+'
df3 = df3.reindex(index=df3.index[::-1])
df3.columns = nach_range
df3.columns.name = 'Transient Na+'
    
plot_heatmap(df1, title='First AP halfwidth (ms)', xlabel='Transient Na+ conductance (S/cm^2)', ylabel='High-threshold K+ conductance (S/cm^2)', output_filename='HTvsNach-AP1_heatmap.png')

plot_heatmap(df2, title='Second AP halfwidth (ms)', xlabel='Transient Na+ conductance (S/cm^2)', ylabel='High-threshold K+ conductance (S/cm^2)', output_filename='HTvsNach-AP2_heatmap.png')

plot_heatmap(df3, title='Spike count', xlabel='Transient Na+ conductance (S/cm^2)', ylabel='High-threshold K+ conductance (S/cm^2)', output_filename='HTvsNach-spikecount_heatmap.png')

