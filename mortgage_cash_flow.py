"""
Mortgage Cash Flow Pricing - Engine
Author: William Carpenter

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
def cash_flow(settle, cpn, wam, term, balloon, \
                       io, delay, speed, prepay_type, bal) -> pd.DataFrame:
    
    """
    Cash flow engine.
    
    Generate generic mortgage cash flows with various prepayment speeds.
    
    Prepay types:
        CPR: conditional prepayment rate

    Assume 30/360 interest rate convention for simplicity.
    Assume mortgage pool pay delay is 15 days for the investor. 
    
    Return an array of mortgage cash flow and weighted-average life.
    
    """
    
    cols = ['Date','Period', 'Starting Balance', 'Interest', 'Scheduled Principal', \
            'Unscheduled Principal', 'Cash Flow', 'Ending Balance']
    
    orig_bal = bal
    settle   = pd.to_datetime(settle, format="%m/%d/%Y")
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
    
    table   = pd.DataFrame(index=range(balloon), columns=cols)

    for i in range(1, balloon+1):
        
        mtg_payment = bal*cpn/100*30/360* \
                      ((1+cpn/100*30/360)**(wam)) \
                      /((1+cpn/100*30/360)**(wam)-1)
        
        smm = 1-(1-speed/100)**(1/12)  # calculate SMM given a CPR

        pay_month = cf_date - DateOffset(months=1)
        
        
        table.iloc[i-1,0] = pay_month
        table.iloc[i-1,1] = i       # period number
        table.iloc[i-1,2] = bal  

        interest = month_days/360*cpn/100*bal
        
        # mortgage payment 
        if i < io + 1:
            principal = 0
        else:
            principal = mtg_payment - interest 
        
        if i == balloon:
            prepay = bal - principal   # rest of remaining balance
            paid_down = True
        else:
            prepay = smm*(bal - principal)
        
        # Edge case where balance hits zero before balloon?        
        if bal - interest - principal - prepay < 0:
            
            paid_down = True

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
                
        table.iloc[i-1,3] = interest
        table.iloc[i-1,4] = principal
        table.iloc[i-1,5] = prepay
        table.iloc[i-1,6] = cash_flow
        table.iloc[i-1,7] = bal
        
        cf_date = cf_date + DateOffset(months=1)
        
        # Exit if mortgage is fully paid down in the period now 
        if paid_down: 
            pay_index = i
            break
    
    # Table and adjust final size for unused months before balloon
         
    return table

def wal(settle, cf) -> float:
    
    '''
    Calculate weighted-average-life of a mortgage cash flow.
    
    Check variables first. 
    If zero or negative - raise an exception error.
    
    '''
    
    settle       = pd.to_datetime(settle, format="%m/%d/%Y")
    cf['settle'] = settle
    cf['diff']   = (pd.to_datetime(cf['Date']) - cf['settle']).dt.days
    
    num          = (cf['diff']*((cf['Scheduled Principal'] + cf['Unscheduled Principal']))).sum()
    denom        = (cf['Scheduled Principal'] + cf['Unscheduled Principal']).sum()          
    wal          = num/denom*1/365
         
    return wal



#%%









    






 
    

    









