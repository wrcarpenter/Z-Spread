"""
Bond Pricing Engine - Z-Spread, I-Spread, Duration
Author: William Carpenter

Also contains engine for I-spread (interpolated spread). 

"""
# Custom modules
import mortgage_cash_flow as mbs  # custom module cash flow engine
import bond_price as px
# Python packages
import datetime
from scipy.optimize import newton
import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset
    
def price(cf, curve, settle, spread, typ) -> float:
    
    """
    Bond Pricing Engine.
    
    Currently can solve for price given a bond I-spread or Z-Spread.
    Assumes provided cashflows are monthly. 
    

    Spread Types:
        Z-Spread -> spot rate yield spread
        I-Spread -> interpolated treasuries
    
    Parameters
    ------------
    cf     : dataframe of cash flows
    curve  : yield or spot rate curve
    settle : bond settle date     
    spread : Z or I spread
    typ    : defining if Z or I spread
    
    Returns:
    ------------
    Bond dollar price as a float
    
    """        
    # Cashflow characteristics given in provided dataframe 
    rate     = cf["Rate"].loc[0]
    curr     = cf["Starting Balance"].loc[0]
    delay    = cf["Pay Delay"].loc[0]

    # Handling settle dates and accrued interest 
    settle   = pd.to_datetime(settle, format="%m/%d/%Y")
    month    = (settle + DateOffset(months=1)).to_pydatetime() # this works 
    pay      = datetime.datetime(month.year, month.month, delay-29)  

    accrued  = (settle.to_pydatetime() - datetime.datetime(settle.year, settle.month, 1)).days
    days_pay = (pay - settle.to_pydatetime()).days
    accr_int = accrued/360*rate/100*curr
        
    mey  = monthly_equiv_yld(settle, cf, curve, spread)
    
    months   = np.array((cf["Period"] - 1).astype(int))
    cf_flow  = np.array((cf["Cash Flow"]).astype(float))
    
    # Z-Spread calculation 
    if typ == "Z":
        
        # Extract correctly sized spot curve - assume monthly cashflows
        spots  = np.array(curve.iloc[0,0:len(cf)])
        # Calculate z rates on each point of the spot curve
        z_rate = spots + spread/100
        # Calculate discount rates
        z_zcb  = 1/((1+z_rate/(12*100))**(months))
        # Price bond 
        price  = (np.sum(cf_flow*z_zcb)-accr_int)*\
                  100/curr*1/(1+mey/100*days_pay/360)
                  
    # I-Spread calculation 
    elif typ == "I":
         
        price = (np.sum(cf_flow/((1+mey/(12*100))**(months)))\
                  -accr_int)*100/curr*1/(1+mey/100*days_pay/360)
    
    return price


def monthly_equiv_yld(settle, cf, curve, spread) -> float:
    
    tenor = mbs.wal(settle, cf)*12
    m     = pd.DataFrame(curve.columns.values.astype(int), columns=["Months"])
    
    # Points for interpolation
    index = m["Months"].gt(tenor).idxmax()
    m_ub  = m["Months"].iloc[index]   
    m_lb  = m["Months"].iloc[index-1]
    y_ub  = curve.iloc[0,index]
    y_lb  = curve.iloc[0,index-1]
    # Linear interpolation
    intrp = y_lb + (tenor - m_lb)*((y_ub - y_lb)/(m_ub - m_lb))
    
    # Bond equivalent yield at WAL point 
    bond_equiv    = intrp + spread/100
    # Monthly equivalent yield
    monthly_equiv = 12*((1+bond_equiv/(2*100))**(2/12)-1)*100
    
    return monthly_equiv
     
    
def spread_solver(spread, cf, curve, settle, px, typ):
        
    """
    Newton Root Finding Function - Solving for bond spread
    """
    
    solver = price(cf, curve, settle, spread, typ)  # using a spread to solve for spread   
    
    return (solver - px)

    
def spread(cf, curve, settle, px, typ) -> float:
    
    """
    Bond Spread
    """    
    # Solver to calculate Z-spread
    # Constants
    s0    = 100
    miter = 1000
    
    sp = newton(spread_solver, s0, args=(cf, curve, settle, px, typ), maxiter=miter)
    
    return sp
    

def duration(settle, cf, curve, spread) -> float:
    
    # Solve for monthly equivalent yield
    mey = monthly_equiv_yld(settle, cf, curve, spread)
        
    # Formula 
    dur = np.sum(net_flow/((1+mey/(12*100))**(months))*1/(1+mey/100*days_to_pay/360)*cf_table[:,6] / np.sum(net_flow/((1+mey/(12*100))**(months))*1/(1+mey/100*days_to_pay/360))) 
    
    return dur

# Unit Testing 
if __name__ == "__main__":
    
    # Get data
    ylds  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/ylds-semi-annual.csv")
    spots = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/spots-monthly.csv")
    
    # I-curve
    i_curve = ylds.loc[ylds['Date']=='3/8/2024']
    i_curve = i_curve.drop("Date", axis=1)
    
    # Z-curve
    z_curve = spots.loc[spots['Date']=='3/8/2024']
    z_curve = z_curve.drop("Date", axis=1)
    
    # Cashflows
    cf_7cpr     = mbs.cash_flow('03/29/2024', 6.50, 360, 360, 240, 0, 54,  7, 'CPR', 1000000)
    cf_7cpr_wal = mbs.wal('03/29/2024', cf_7cpr)
    
    # Getting prices
    px_i      = price(cf_7cpr, i_curve, "03/29/2024", 172, "I")
    px_z      = price(cf_7cpr, z_curve, "03/29/2024", 140, "Z")
    
    print(px_i)
    print(px_z)





