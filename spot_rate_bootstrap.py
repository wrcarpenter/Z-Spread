"""
Bootstrap Spot Rate Curve

Code for parsing treasury data, bootstrapping a spot rate curve, and generating
various charts.

Author: Will Carpenter

"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline

# Generate interpolated yields data
def interpolate_yields(tsy, head) -> pd.DataFrame:
    
    """
    Treasury Yields - Semi-Annual Frequency 
    
    Uses cubic spline interpolation.
    
    """
    
    ylds   = np.empty([1,62])
    months = np.array([1,2,3,5,6,12,24,36,60,84,120,240,360])
    x      = np.linspace(0,360,61)
    
    tsy_cols = list(tsy.columns.values)
    cols     = list(head.columns.values)
    
    for i in range(len(tsy)):
        
        row = np.array(tsy.loc[i])
        date = row[0:1]    
        rates = row[1:]
        
        f = CubicSpline(months, rates)
        interp = f(x)
        
        add  = np.append(date, interp)
        ylds = np.vstack((ylds, add))
        
    ylds = pd.DataFrame(np.delete(ylds, 0, 0), columns=cols)  
    
    return ylds

    
def spot_rate_bootstrap(ylds, tsy, head) -> pd.DataFrame:
    
    cols     = list(head.columns.values)
    spots = pd.DataFrame(np.zeros((ylds.shape[0], ylds.shape[1]), dtype=float), columns=cols)
     
    # No interpolation required here - shorter-term treasuries are ZCBs
    spots['Date'] = tsy['Date']
    spots['0']    = tsy['1']
    spots['6']    = tsy['6']
    spots['12']   = tsy['12']
    
    # Treasury bond assumptions for bootstrap; do not modify
    face   = 100
    delta  = 1/2 
    
    # Bootstrap methodology 
    for row in range(0,spots.shape[0]):  
        for col in range(0, spots.shape[1]):
            
            if col <= 3: continue # spot rates already defined for shorter bonds
            
            # Now solving for zero-coupon bond yield
            int_cf = 0 
            cpn    = ylds.iloc[row, col]  # interpolated coupon for par bond
            
            for i in range(2, col): # solve for intermediate cash flows
                        
                zcb    = 1/((1+spots.iloc[row, i]/100*delta)**(i-1)) 
                int_cf = int_cf +cpn/100*delta*face*zcb
                    
            zero = ((face + face*cpn/100*delta)/(face - int_cf)) # algebra to solve for zero rate
            zero = zero**(1/(col-1))
            zero = (zero-1)*2
            
            spots.iloc[row, col] = zero*100
    
    return spots

# Converting semi-annual spots to monthly using spline interpolation
def spot_rates_monthly(spots):
    
    spots_monthly = np.empty([1,361])
    months        = np.array(spots.columns.to_list())
    months        = months[1:]
    x             = np.linspace(0,360,360)
    
    for i in range(len(spots)):
        
        row   = np.array(spots.loc[i])
        date  = row[0:1]
        rates = row[1:]
        
        f = CubicSpline(months, rates)
        interp = f(x)
        
        add = np.append(date, interp)
        spots_monthly = np.vstack((spots_monthly, add))
    
    
    months = ["Date"] + np.arange(1,361,1).tolist()
    
    spots_monthly = pd.DataFrame(np.delete(spots_monthly, 0, 0), columns=months)  

    return spots_monthly     
      
if __name__ == "__main__":
    
    # Read in par-yield data via Github
    tsy  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-rates.csv", header=0)
    head = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-spot-header.csv")
    
    # Generate data 
    ylds          = interpolate_yields(tsy, head)
    spots         = spot_rate_bootstrap(ylds, tsy, head)
    spots_monthly = spot_rates_monthly(spots)
    
    # Save down relevant data 
    # ylds.to_csv('C:/Users/wcarp/OneDrive/Desktop/Z-Spread/Data/ylds-semi-annual.csv', index=False)  
    # spots.to_csv('C:/Users/wcarp/OneDrive/Desktop/Z-Spread/Data/spots-semi-annual.csv', index=False)
    # spots_monthly.to_csv('C:/Users/wcarp/OneDrive/Desktop/Z-Spread/Data/spots-monthly.csv', index=False)

