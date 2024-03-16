"""
Mortgage Cash Flows
W Carpenter
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline

#%%

# Generic methodology to create mortgage cashflows
def mortgage_cash_flow(settle, cpn, wam, term, ballon, io, delay, prepay, bal):
    
    """
    Assume 30/360 interest rate convention for simplicity.
    Assume mortgage pool pay delay is 25 days for the investor.  
    
    """
    
    mtg_payment = bal*cpn/100*30/360* \
                  ((1+cpn/100*30/360)**(amort)) \
                  /((1+gross/100*30/360)**(amort-1))
    
    # intialize variables
    
    schedule_princ = 0
    interest       = 0
    prepay         = 0
    cash_flow      = 0
    discounted_cf  = 0
    wal            = 0
    principal      = bal                 
    
    cf_table    = np.empty((balloon,7))
    cf_table[:] = np.nan
    
    for i range(1, balloon+1):
        
        pay_month = 
    
def z_spread(cash_flow, spot_rates, price):
    continue


def price(cash_flow, spot_rates, z_spread):
    continue    
    
#%%



 
    

    









