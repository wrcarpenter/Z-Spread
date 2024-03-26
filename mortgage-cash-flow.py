"""
Mortgage Cash Flow Pricing
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
def mortgage_cash_flow(settle, cpn, wam, term, balloon, \
                       io, delay, speed, prepay_type, bal) -> pd.DataFrame:
    
    """
    Generate generic mortgage cash flows with various prepayment speeds.
    
    Prepay types:
        CPR: conditional prepayment rate
        PSA: public securities association standard

    Assume 30/360 interest rate convention for simplicity.
    Assume mortgage pool pay delay is 25 days for the investor. 
    
    Return an array of mortgage cash flow and weighted-average life.
    
    """
    
    cols = ['Period', 'Starting Balance', 'Interest', 'Scheduled Principal', \
            'Unscheduled Principal', 'Cash Flow', 'Ending Balance']
    
    orig_bal = bal
    settle   = pd.to_datetime(settle, format="%m/%d/%Y")
    settle   = settle.to_pydatetime()
    cf_month = settle + DateOffset(months=1)
    cf_date  = datetime.datetime(cf_month.year, cf_month.month, delay)
    
    # Intialize variables    
    schedule_princ = 0
    interest       = 0
    prepay         = 0
    cash_flow      = 0
    discounted_cf  = 0
    wal            = 0
    principal      = bal
    paid_down      = False
    pay_index      = 0
    month_days     = 30    # assume a 30/360 interest accrual               
    
    cf_table    = np.empty((balloon,8))
    cf_table[:] = np.nan
    
    for i in range(1, balloon+1):
        
        mtg_payment = bal*cpn/100*30/360* \
                      ((1+cpn/100*30/360)**(wam)) \
                      /((1+cpn/100*30/360)**(wam)-1)
        
        SMM = 1-(1-speed/100)**(1/12)  # calculate SMM given a CPR

        pay_month = cf_date - DateOffset(months=1)

        date_add = pay_month.strftime("%m/%d/%Y")
        print(type(date_add))
        
        cf_table[i-1,0] = i       # period number
        cf_table[i-1,1] = bal              
                        
        interest = month_days/360*cpn/100*bal
        
        # mortgage payment 
        if i < io + 1:
            principal = 0
        else:
            principal = mtg_payment - interest 
        
        if i == balloon:
            prepay = bal - principal   # rest of remaining balance
        else:
            prepay = SMM*(bal - principal)
        
        # Edge case where balance hits zero before balloon 
        
        if bal - interest - principal - prepay < 0:

            if bal - interest - principal <  0:
                principal = bal - interest - 0 
                prepay    = 0 
                bal = 0 
            
            else:
                principal = bal - interest
                prepay = bal - interest - principal - 0 
                bal = 0
                
        else:

            bal = bal - principal - prepay 

        cash_flow = interest + principal + prepay
        days_from_settle = (cf_date - settle).days
        wal = (principal + prepay)*days_from_settle/orig_bal*1/365 + wal
        wam = wam - 1
        
        # populate table
        # current balance
        cf_table[i-1,2] = interest
        cf_table[i-1,3] = principal
        cf_table[i-1,4] = prepay
        cf_table[i-1,5] = cash_flow
        cf_table[i-1,6] = bal
        cf_table[i-1,7] = date_add
        
        
        cf_date = cf_date + DateOffset(months=1)
        
        # Exit if mortgage is fully paid down in the period now 
        if paid_down: 
            pay_index = i
            break
    
    # Table and adjust final size for unused months before balloon         
    cf_table = pd.DataFrame(cf_table[0:i,:], columns=cols)   
            
    return cf_table

def mortgage_wal(settle, cf) -> float:
    
    '''
    Calculate weighted-average-life of a mortgage cash flow.
    '''
    
    settle    = pd.to_datetime(settle, format="%m/%d/%Y")
    settle    = settle.to_pydatetime()
    
    cf['WAL'] = 0
    
    
    # need settle date to determine period of time between cash flow and present
    
        
#%%
# Unit Testing Mortgage Cash flows 
# Returns an array with mortgage cash flows

# Unit Testing 
cf_0cpr  = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 15,  0, 'CPR', 500000)
cf_5cpr  = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 15,  5, 'CPR', 500000)
cf_20cpr = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 15, 25, 'CPR', 500000)
cf_40cpr = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 15, 40, 'CPR', 500000)



#%%
# Charting cash flows

def mortgage_cf_chart(cf):
    










    






 
    

    









