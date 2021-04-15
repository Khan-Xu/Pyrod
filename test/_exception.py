# -*- coding: utf-8 -*-

from __future__ import absolute_import

"""The exception class"""

class The_Parameter_Exception(Exception):
    """The exception for the parameters of model construction."""

class The_Data_Load_Exception(Exception):
    """The exception for data loading."""

class The_Data_Base_Exception(Exception):
    """The exception for the parameters not included in database."""

class The_Data_Check_Exception(Exception):
    """The exception for the check of raw data."""

class The_Vars_Check_Exception(Exception):
    """The exception for the check of input Vars."""