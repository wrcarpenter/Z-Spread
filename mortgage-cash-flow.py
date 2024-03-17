"""
Mortgage Cash Flow
W Carpenter
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline
import datetime            # working with dates
import calendar            # working with days 
from pandas.tseries.offsets import DateOffset

#%%

# Generic methodology to create mortgage cashflows
def mortgage_cash_flow(settle, cpn, wam, term, balloon, io, delay, prepay, prepay_type, bal):
    
    """
    Generate generic mortgage cash flows with various prepayment speeds.
    
    Prepay types:
        CPR: conditional prepayment rate
        PSA: public securities association standard

    Assume 30/360 interest rate convention for simplicity.
    Assume mortgage pool pay delay is 25 days for the investor. 
    
    Return an array of mortgage cash flow and weighted-average life.
    
    """
    
    orig_bal = bal
    settle   = pd.to_datetime(settle, format="%m/%d/%Y")
    settle   = settle.to_pydatetime()
    cf_month = settle + DateOffset(months=1)
    cf_date  = datetime.datetime(cf_month.year, cf_month.month, delay-29)
    
    # Accrued interest 
    
    mtg_payment = bal*cpn/100*30/360* \
                  ((1+cpn/100*30/360)**(wam)) \
                  /((1+cpn/100*30/360)**(wam-1))
    
    # intialize variables    
    schedule_princ = 0
    interest       = 0
    prepay         = 0
    cash_flow      = 0
    discounted_cf  = 0
    wal            = 0
    principal      = bal                 
    
    cf_table    = np.empty((balloon,6))
    cf_table[:] = np.nan
    
    for i in range(1, balloon+1):
        
        pay_month = cf_date - DateOffset(months=1)
        
        month_days = 30  # assume 30/360 interest convention 
        
        interest = month_days/360*cpn/100*bal
        
        if i < io +1: 
            principal = 0
        else:
            principal = mtg_payment - interest
        
        if i == balloon:
            prepay = bal - principal 
        
        else:
            prepay = 0
            
        bal = bal - principal - prepay 
        cash_flow = interest + principal + prepay
        days_from_settle = (cf_date - settle).days
        wal = (principal + prepay)*days_from_settle/orig_bal*1/365 + wal
        # populate table
        
        cf_table[i-1,0] = i           # period number
        cf_table[i-1,1] = bal         # current balance
        cf_table[i-1,2] = interest
        cf_table[i-1,3] = principal
        cf_table[i-1,4] = prepay
        cf_table[i-1,5] = cash_flow
        
        cf_date = cf_date + DateOffset(months=1)
        
        
     
        
    cols = ['Period', 'Current Balance', 'Interest', 'Scheduled Principal', 'Unscheduled Principal', 'Cash Flow']
     
    cf_table = pd.DataFrame(cf_table, columns=cols)   # completed yields array 
        
    return cf_table

# def mortgage_wal(cf, settle):
    #continue
    
    # calculate mortgage weighted average life

    
#%%

# Returns an array with mortgage cash flows 
cf = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 45, 0, 'CPR', 1000000)


#%%
# Visualizing Mortgage cash-flows 


def mortgage_cf_chart():
    






 
    

    









