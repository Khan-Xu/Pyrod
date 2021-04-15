# -*- coding: utf-8 -*-

from __future__ import absolute_import
#----------LIBRARYS-----------

# exceptions library
from _exception import (The_Data_Check_Exception)
# python processing library  
import numpy as np
# private library 
import _check_data

#----------CONSTANTS----------

class data_raw(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check(self):
        _check_data._check_array(self.x)
        _check_data._check_array(self.y)
        _check_data._check_length(self.x, self.y)

    def interp(self, density = 100):

        if not isinstance(density, int):
            raise The_Data_Check_Exception("The density must be an int type")

        qs = round(self.x[ 0] * density)/density
        qe = round(self.x[-1] * density)/density
        q0 = 0.0

        interped_q = np.linspace(q0, qe, int((qe - q0)*density) + 1)
        intensity = np.interp(interped_q, self.x, self.y)
        intensity[0 : int(qs * intensity)] = 0

        self.x = interped_q
        self.y = intensity