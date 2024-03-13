"""
Bootstrap Spot Rate Curve
W Carpenter
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline

#%%
# Read in par-yield data
tsy  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-rates.csv", header=0)
head = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-spot-header.csv")
cols = list(head.columns.values)

#%%
# Generate interpolated yields data
ylds   = np.empty([1,62])
months = np.array([1,2,3,5,6,12,24,36,60,84,120,240,360])
x      = np.linspace(0,360,61)

for i in range(len(tsy)):
    
    row = np.array(tsy.loc[i])
    date = row[0:1]    
    rates = row[1:]
    
    f = CubicSpline(months, rates)
    interp = f(x)
    
    add  = np.append(date, interp)
    ylds = np.vstack((ylds, add))
    
ylds = pd.DataFrame(np.delete(ylds, 0, 0), columns=cols)   # completed yields array

#%%
# rows, cols 
spots = pd.DataFrame(np.zeros((ylds.shape[0], ylds.shape[1]), dtype=float), columns=cols)
 
# A portion of the par-yield curve already contains spot rates because bonds 1-year are zcb

# No interpolation required here - shorter-term treasuries are ZCBs
spots['Date'] = tsy['Date']
spots['0']    = tsy['1']
spots['6']    = tsy['6']
spots['12']   = tsy['12']

# Bond assumptions, do not need to be modified
face   = 100
delta  = 1/2 

# Bootstrap methodology - create semi-annual
for row in range(0,spots.shape[0]):  
    for col in range(0, spots.shape[1]):
        
        if col <= 3: continue # spot rates already defined 
        
        # Now solving for zero-coupon bond yield
        int_cf = 0 
        cpn    = ylds.iloc[row, col]  # interpolated coupon for par bond
        
        for i in range(2, col): # now solve for intermediate cash flows
                    
            zcb    = 1/((1+spots.iloc[row, i]/100*delta)**(i-1))
            int_cf = int_cf +cpn/100*delta*face*zcb
                
        zero = ((face + face*cpn/100*delta)/(face - int_cf)) # algebra to solve for zero rate
        zero = zero**(1/(col-1))
        zero = (zero-1)*2
        
        spots.iloc[row, col] = zero*100

# now create a fully interpolated zero rate table for ease of usage 
# use spline interpolation again here

#%% 





# Plotting 

# add ZCB prices 
# add a curve 
# add curve overtime 




