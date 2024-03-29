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
# semi-annual data 
curve = ylds.loc[ylds['Date']=='3/8/2024']
curve = curve.drop("Date", axis=1)

tenor = pd.DataFrame(curve.columns.values.astype(int))

#%%

sprd  = price(cf_10cpr, curve, "03/01/2024", 100, "I")

#%%

#%%

def duration(cf, settle, mey) -> float:
    
    return 0
    


#%%

def price(cf, curve, settle, spread, spread_type) -> float:
    
    # for monthly cashflows
    
    # assume i-spread for now 
    tenor = mbs.wal(settle, cf)*12
    m     = pd.DataFrame(curve.columns.values.astype(int), columns=["Months"])
    
    index = m["Months"].gt(tenor).idxmax()
    m_ub  = m["Months"].iloc[index]   
    m_lb  = m["Months"].iloc[index-1]
    y_ub  = curve.iloc[0,index]
    y_lb  = curve.iloc[0,index-1]
    
    intrp = y_lb + (tenor - m_lb)*((y_ub - y_lb)/(m_ub - m_lb))
    bey   = intrp + spread/100
    mey   = 12*((1+bey/(2*100))**(2/12)-1)*100
    
    print(tenor, index, m_ub, m_lb, bey, mey)
    
    months = 
    
    
    
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
    # get wal
    # get an index 
    # get bounds
    # interpolation formula
    
    return 0

        







