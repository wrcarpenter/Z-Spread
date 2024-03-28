# -*- coding: utf-8 -*-
"""
Z-Spread Calculation

Also contains engine for I-spread (interpolated spread). 

"""
# Packages/modules
import mortgage_cash_flow as mbs  # custom module cash flow engine
import bond_price as px

#%%
# Import yield data 
ylds = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/ylds-semi-annual.csv")
    
#%%
# Create bond cash flow 

cf_10cpr  = mbs.cash_flow('03/01/2024', 6.50, 360, 360, 120, 0, 15,  10, 'CPR', 100000)
wal       = mbs.wal('03/01/2024', cf_10cpr)

# Create curve for I-spread
# pandas dataframe of index
# semi-annual data 
curve = ylds.loc[ylds['Date']=='3/8/2024']
curve = curve.drop("Date", axis=1)

#%%


#%%

def duration(cf, settle, mey) -> float:
    


#%%

def price(cf, curve, settle, spread, spread_type) -> float:
    
    
    return 0

def z_spread(cf, curve, settle, price) -> float:
    
    """
    Z-Spread 
    
    """
    return 0
 

def i_spread(cf, curve, settle, price) -> float:
    
    """
    I-Spread 
    
    Parameters
    -----------
    cf     : pd.dataframe of cash flow data
    curve  : Treasury yield curv ** semiannual data
    settle : settle date as a string
    price  : bond price as a float 
    
    Returns
    -----------
    I-spread as a float (interpolated yield spread)
    
    """
    
    wal = mbs.wal(settle, cf)
    print(wal)
    
    # get wal
    # get an index 
    # get bounds
    # interpolation formula
    
    return 0
        
def interp(p1, p2) -> float:
    
    return 0
    
    """
    Linear Yield Interpolation

    Parameters
    -----------
    p1 : Point 1 
    p2 : Point 2

    Returns 
    -----------
    Interpolated yield point (linear) 

    """
        







