# -*- coding: utf-8 -*-

from __future__ import absolute_import

"""----- LIBRARY -----"""

# exceptions library
from _exception import (The_Parameter_Exception, The_Data_Base_Exception, The_Vars_Check_Exception)

# Python stdlib imports
import datetime
import re
import os

# data processing library
import numpy as np
import pandas as pd

# pyrod library
import _data_base

"""----- CONSTANT -----"""
"""----- CLASSES ------"""

class model_substrate(object):

    def __init__(self, A = 'Sr2+', B = 'Ti4+'):

        self.ABO3 = [A, B, 'O2-']




