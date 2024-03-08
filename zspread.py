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
# Create zero-coupon yields via bootstrapping 
# create an empty pandas array of same size 
# start a loop that performs the calculation 
# then add the resulting zero yield as you bootstrapping 

spots = pd.DataFrame(np.zeros((ylds.shape[0], ylds.shape[1]), dtype=float), columns=cols)

# assign same colums 

# A portion of the par-yield curve already contains spot rates because bonds 1-year and under do 
# not pay an intermediate coupon 

spots['Date'] = ylds['Date']
spots['0']    = ylds['1']
spots['6']    = ylds['6']
spots['12']   = ylds['12']


for row in len(spots):
    





#%%

# Create a bond cash-flow - start with a mortgage that pays principal/interest assuming 30/360 convention 







#%% 
