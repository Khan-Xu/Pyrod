# -*- coding: utf-8 -*-

#%%
from __future__ import absolute_import
#----------LIBRARYS-----------

# exceptions library
from _exception import (The_Parameter_Exception, The_Data_Load_Exception, The_Data_Base_Exception)
# python stdlib library
import os
import pickle
# python processing library  
import numpy as np
import pandas as pd

#----------CONSTANTS----------

try:
    # atomic_form_factor.xlsx atomic_mass.xlsx and atomic_scattering_facotr.pickle
    ATOMIC_FORM_FACTOR = os.path.abspath(os.path.dirname('atomic_form_facotr.xlsx')) + '/base/atomic_form_factor.xlsx'
    ATOMIC_MASS = os.path.abspath(os.path.dirname('atomic_mass.xlsx')) + '/base/atomic_mass.xlsx'
    ATOMIC_SCATTERING_FACTOR = os.path.abspath(os.path.dirname('atomic_scattering_factor.pickle')) + '\\base\\atomic_scattering_factor.pickle'

    # loading to python vars
    IONS_TABLE = pd.read_excel(ATOMIC_FORM_FACTOR, sheet_name = 'atomic_form_factor', index_col = 0)
    ATOM_TABLE = pd.read_excel(ATOMIC_MASS, sheet_name = 'Sheet1', index_col = 0)

    ASF_file = open(ATOMIC_SCATTERING_FACTOR, 'rb')
    ASF_TABLE = pickle.load(ASF_file)
    ASF_file.close()

    IONS_LIST = IONS_TABLE.index.values.tolist()
    ATOM_LIST = ATOM_TABLE.index.values.tolist()

except The_Data_Load_Exception:
    print('Data base loading fail. Used library: pandas; pickle')

#----------FUNCTIONS----------

def _check_ions(ion):
    if isinstance(ion, str):
        if ion not in IONS_LIST:
            raise The_Data_Base_Exception("The ion is not included in database 'atomic_form_factor.xlsx'")
    else:
        raise The_Parameter_Exception("The input parameter 'ion' should be string")

def _check_atom(atom):
    if isinstance(atom, str):
        if atom not in ATOM_LIST:
            raise The_Data_Base_Exception("This ion is not included in database 'atomic_mass.xlsx'")
    else:
        raise The_Parameter_Exception("The input parameter 'atom' should be string")
#%%

  