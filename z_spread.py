"""
Bond Pricing Engine
Author: William Carpenter

Also contains engine for I-spread (interpolated spread). 


"""
# Packages/modules

import mortgage_cash_flow as mbs  # custom module cash flow engine
import bond_price as px
import datetime as dt
    
#%%
# Testing
ylds  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/ylds-semi-annual.csv")
spots = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/spots-monthly.csv")

i_curve = ylds.loc[ylds['Date']=='3/8/2024']
i_curve = curve.drop("Date", axis=1)

z_curve = spots.loc[spots['Date']=='3/8/2024']
z_curve = z_curve.drop("Date", axis=1)

# Verified --
cf_7cpr  = mbs.cash_flow('03/29/2024', 6.50, 360, 360, 240, 0, 54,  7, 'CPR', 1000000)
print(mbs.wal('03/29/2024', cf_7cpr))

px_i      = price(cf_7cpr, i_curve, "03/29/2024", 100, "I")
px_z      = price(cf_7cpr, z_curve, "03/29/2024", 100, "Z")

#%%




#%%

def price(cf, curve, settle, spread, typ) -> float:
    
    """
    Bond Pricing Engine.
    
    Currently can solve for price given a bond I-spread. 

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
    
    # Cash flow characteristics 
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
        
    months   = np.array((cf["Period"] - 1).astype(int))
    cf_flow  = np.array((cf["Cash Flow"]).astype(float))
        
    price    = (np.sum(cf_flow/((1+mey/(12*100))**(months))) \
                -accr_int)*100/curr*1/(1+mey/100*days_pay/360)
    
    return price

def z_spread(cf, curve, settle, price) -> float:
    
    """
    Z-Spread 
    
    """
    
    # solve for a price with Z-spread and use Newton to solve it to equal given a price
    
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


def duration(cf, settle, mey) -> float:
    
    # once you have a MEY ... duration should not depend on Z or I spread 
    
    return 0



