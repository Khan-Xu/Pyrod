# -*- coding: utf-8 -*-

from __future__ import absolute_import
#----------LIBRARYS-----------

# exceptions library
from _exception import (The_Parameter_Exception, The_Vars_Check_Exception)
# python processing library  
import numpy as np
# private library 
import _check_data

#----------CONSTANTS----------
#----------FUNCTIONS----------

# Roughness

def _robinson_roughness(beta_r, x):

    """[1]. Robinson, Ian K. "Crystal truncation rods and surface roughness." Physical Review B 33.6 (1986): 3830."""

    if beta_r < 0:
        raise The_Vars_Check_Exception("The robinsion_roughness factor should be positive")
    robinson_factor = (1 - beta_r)/((1 - beta_r)**2 + 4 * beta_r * (np.sin(np.pi * x)**2))**0.5 # Cubic phase

    return robinson_factor

def _interface_roughness(beta_i, x):

    """interface roughness model, used for small angle relfection"""

    if beta_i < 0:
        raise The_Vars_Check_Exception("interface_roughness factor should be positive")
    interface_factor = np.exp(-1 * (beta_i * x))

    return interface_factor

# Vacancy

def _gradient_vacancy(alpha_g, vancy_0, vancy_1, layer_num):

    """[1]. Druce, J., et al. "Surface termination and subsurface restructuring of perovskite-based solid oxide electrode materials." Energy & Environmental Science 7.11 (2014): 3593-3599."""

    if vancy_0 < 0 or vancy_1 < 0 or alpha_g < 0:
        raise The_Vars_Check_Exception("Expected positve vacancy factors")
    if vancy_0 > 1 or vancy_1 > 1:
        raise The_Vars_Check_Exception("The denstiy of vacancy should below 1")

    vancy_s, vancy_e = np.max([vancy_0, vancy_1]), np.min([vancy_0, vancy_1])
    a = (vancy_s - vancy_e)/(np.exp(-1* alpha_g *(range(layer_num - 1)) - 1))
    b = vancy_e - a
    vacancy_factor = a + b * np.exp(-1 * np.array(layer_num))

    return vacancy_factor

def _O2_vacancy(layers, ocupation, vancy_o2):

    """The vacancy of O2-"""

# Relaxation



