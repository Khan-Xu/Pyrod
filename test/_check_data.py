# -*- coding: utf-8 -*-

from __future__ import absolute_import
#----------LIBRARYS-----------

# exceptions library
from _exception import (The_Data_Check_Exception)
# python stdlib library
import six
# python processing library  
import numpy as np

#----------CONSTANTS----------
#----------FUNCTIONS----------

def _check_array(array, dtype = "numeric", force_all_finite = True):

    array_orig = np.asarray(array) # the reference to original array
    dtype_numeric = isinstance(dtype, six.string_types) and dtype == "numeric"
    dtype_orig = getattr(array, "dtype", None)

    if not hasattr(dtype_orig, 'kind'):
        dtype_orig = None # check if pandas dataframe

    dtype_multi_orig = None # check if the object contains several dtypes (typically a pandas dataframe)

    if hasattr(array, "dtypes") and hasattr(array, "__array__"):
        dtypes_orig = np.array(array.dtypes)

    if hasattr(array, 'dtype') and array.dtype is not None and hasattr(array.dtype, 'kind') and array.dtype.kind == "c":
        raise The_Data_Check_Exception("Complex data not supported!")

    try:
        finite_check = np.isfinite(np.sum(array_orig))
        if not finite_check:
            raise The_Data_Check_Exception("array contains infinite number element")
    except:
        raise The_Data_Check_Exception("array contains non-number element")

    if not array.ndim == 1:
        raise The_Data_Check_Exception("Excepted 1D array, got non-1D array instead")
    
def _check_length(x, y):

    if not np.sum(np.shape(x)) == np.sum(np.shape(y)):
        raise The_Data_Check_Exception("Excepted equal length arrays (x, y), got non-equal-length arrays instead")

#-----------CLASSES-----------