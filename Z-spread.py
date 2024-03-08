"""
Z-Spread
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

tsy = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-rates.csv", header=0)

#%%
# Generate interpolated yields data

ylds   = np.empty([1,361])
months = np.array([1,2,3,5,6,12,24,36,60,84,120,240,360])
x      = np.linspace(1,360,360)

for i in range(len(tsy)):
    
    row = np.array(tsy.loc[i])
    date = row[0:1]    
    rates = row[1:]
    
    f = CubicSpline(months, rates)
    interp = f(x)
    
    add  = np.append(date, interp)
    ylds = np.vstack((ylds, add))
    
ylds = pd.DataFrame(np.delete(ylds, 0, 0))   # completed yields array 


#%%

# Create zero-coupon yields



#%%

 
