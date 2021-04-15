# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 23:01:57 2018

@author: USER
"""

import pickle
import os

import numpy as np
import matplotlib.pyplot as plt

import tool.control as tc
import tool.tools as tt

CTR_FACTOR_PATH = os.path.abspath(os.path.dirname('ctr_optimised_result.pickle')) +\
                    '/data/ctr_optimised_result.pickle'
            
CTR_ELECTR_PATH = os.path.abspath(os.path.dirname('ctr_optimised_result.pickle')) +\
                    '/ctr_optimised_result_electron.pickle'

ctr_factor = {}
ctr_electr = {}
    
with open(CTR_FACTOR_PATH, 'rb') as cf, open(CTR_ELECTR_PATH, 'rb') as ce:
    
    unpicklerf = pickle.Unpickler(cf)
    unpicklere = pickle.Unpickler(ce)
    
    ctr_factor = unpicklerf.load()
    ctr_electr = unpicklere.load()

mask = tc.bragg_mask(ctr_factor['q'],3,1,'yin')
amask = tc.bragg_mask(ctr_factor['q'],3,1,'yang')
locate = np.where(mask != 0)[0].tolist()

factor_a = ctr_factor['substrate_ctr'] + ctr_factor['slab_ctr']
electr_a = ctr_electr['substrate_ctr'] + ctr_electr['slab_ctr']
                        
q_mask = ctr_factor['q'][locate]
factor_m = factor_a[locate]
electr_m = electr_a[locate]
data_m = ctr_factor['shkl'][locate]

trans = abs(factor_m)/abs(electr_m)
data_e = data_m/trans

trans_s = tt.savitzky_golay(trans,7,1)
data_s = data_m/trans_s

init = ctr_electr['slab_ctr']
subs = ctr_electr['substrate_ctr']
data = np.interp(ctr_factor['q'], q_mask, data_s)

# expand and add boundary to data
# the length of b_data is 6*length(d) - 3
def b_data(data):

    # conjugate data of imported data
    c_data = np.conj(data[::-1])
    
    # expand the data to conjugate data + data
    # connection part is the arverate
    # ex_c_d -- expanded data    
    ex_data = np.hstack([c_data[0:-1], (c_data[-1] + data[0])/2, data[1:]])
    
    # b_d -- boundary data, add the boundary of ex_c_data
    b_data = np.hstack([np.zeros(len(ex_data)), 
                     ex_data, 
                     np.zeros(len(ex_data))])
    
    return b_data

# boundary mask for expanded and boundary added data
def bdmask(data):
    
    bdmask = np.zeros(6*len(data)-3)
    bdmask[2*len(data):4*len(data)-3] = 1
    
    return bdmask
    
    

def joint_data(experiment_data, fitting_data, limit):
    
    experiment_data_l = experiment_data[limit]
    fitting_data_l = fitting_data[limit]
    
    scale = experiment_data_l/abs(fitting_data_l)
    
    experiment_data[0:limit] = abs(fitting_data[0:limit])*scale
    
    return experiment_data

# inverse fourier transform of dffraction signal with phase
# ifft - inverse fourier transform
# diffraction siganal is the fourier transform of electron distribution
def diffraction2electron(b_d):
    
    # b_d: boudary and expanded diffraction data with phase
    electron = np.fft.ifft(b_d)
    
    return electron

# diffraction signal is the fourier transform of electron distribution
def electron2diffraction(electron):
    
    #should be noted here!
    # Comparae with the origin data, the phase of re fourier transform diffraction data
    # is different! If we want to combine two part of the complex diffraction data
    # re transform them all!!
    
    diffraction = np.fft.fft(electron)
    
    return diffraction

test = joint_data(data, init + subs, 25)

b_substrate_ctr = electron2diffraction(np.fft.ifftshift(diffraction2electron(b_data(subs))))
b_slab_ctr = b_data(init)
b_shkl = b_data(test)
b_mask = b_data(mask)
b_amask = b_data(amask)
b_iq = b_data(ctr_electr['q'])

electron = np.fft.ifftshift(diffraction2electron(b_slab_ctr))
re_slab_ctr = electron2diffraction(electron)

re_electron = diffraction2electron(re_slab_ctr)
rre_slab_ctr = electron2diffraction(re_electron)
rre_electron = diffraction2electron(rre_slab_ctr)
rrre_slab_ctr = electron2diffraction(rre_electron)
rrre_electron = diffraction2electron(rrre_slab_ctr)

###################################################################
# complex data cannot be interpolanted

bm_actr = b_mask*(b_substrate_ctr + b_slab_ctr)
bm_shkl = b_mask*b_shkl

Bq = b_substrate_ctr
s0 = b_slab_ctr
obs = abs(Bq + s0)

gmask = np.zeros(2193)
#gmask[800:1200] = 1
gmask[:] = 1

test_phase = np.random.random(2193)
#
uq = gmask*np.real(electron*test_phase)*np.exp(1j*test_phase)

for i in range(20):
    
    Sq = electron2diffraction(uq)

    Fq = Bq + Sq
    
#    plt.plot(np.log(abs(Fq)))
    
    phase = np.angle(Fq)
    
    cn = np.sum(abs(Fq)*abs(obs))/np.sum(np.square(abs(obs)))

    Tq = cn*abs(obs)*np.exp(1j*phase)-Bq
    
    tq = diffraction2electron(Tq)
    
#    plt.plot(abs(tq))
        
    uq = tq*gmask
    
plt.plot(abs(electron))
plt.plot(abs(uq))

#
#plt.plot(b_iq,bm_shkl)
#plt.plot(b_iq,b_shkl)

#####################################################################