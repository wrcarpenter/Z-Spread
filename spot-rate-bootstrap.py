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
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, MaxNLocator

#%%
# Read in par-yield data
tsy  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-rates.csv", header=0)
head = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-spot-header.csv")

# Define columns 
tsy_cols = list(tsy.columns.values)
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
 
# No interpolation required here - shorter-term treasuries are ZCBs
spots['Date'] = tsy['Date']
spots['0']    = tsy['1']
spots['6']    = tsy['6']
spots['12']   = tsy['12']

# Bond assumptions for bootstrap; do not modify
face   = 100
delta  = 1/2 

# Bootstrap methodology 
for row in range(0,spots.shape[0]):  
    for col in range(0, spots.shape[1]):
        
        if col <= 3: continue # spot rates already defined 
        
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


# update/replace file 
spots.to_csv('C:/Users/wcarp/OneDrive/Desktop/Z-Spread/Data')

#%% 

# Converting semi-annual spots to monthly using spline interpolation
spots_monthly = np.empty([1,361])
months        = np.array(spots.columns.to_list())
months        = months[1:]
x             = np.linspace(1,360,360)

for i in range(len(spots)):
    
    row   = np.array(spots.loc[i])
    date  = row[0:1]
    rates = row[1:]
    
    f = CubicSpline(months, rates)
    interp = f(x)
    
    add = np.append(date, interp)
    spots_monthly = np.vstack((spots_monthly, add))

spots_monthly.to_clipboard()

spots_monthly = pd.DataFrame(np.delete(ylds, 0, 0))        

#%% Plotting (creating custom project plots)

# Plot treasury points
def tsy_rate_plot():
    
    # Define data
    x1 = np.array(tsy_cols[5:])
    x1 = x1.astype(float)
    y1 = np.array(tsy.loc[1])
    y1 = y1[5:]
    # Define figure
    fig, ax = plt.subplots(figsize=(10, 6))
    # Set ticks for x-axis 
    ax.set_xticks(x1)
    ax.set_yticks(np.arange(4.0, 6.0, 0.25))
    # Titling
    ax.set_ylabel('Yield (%)', fontsize="large")
    ax.set_xlabel('Months', fontsize="large")
    ax.set_title('Treasury Par Rates 3/8/24')
    # set text size
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    # Generate plot
    plt.scatter(x1,y1, color="green", marker="s", label='Treasury Par Yields')
    plt.legend(loc='upper right', fontsize='large')            

# Plot interpolated treasury yields
def interp_tsy_yld_plot():            
    
    # Define data
    x1 = np.array(tsy_cols[5:])
    x1 = x1.astype(float)
    x2 = np.array(list(ylds.columns.values))
    x2 = x2[2:].astype(float)
    y2 = np.array(ylds.loc[1])
    y2 = y2[2:]
    
    # Define data 
    x3 = np.array(tsy_cols[5:])
    x3 = x3.astype(float)
    y3 = np.array(tsy.loc[1])
    y3 = y3[5:]
    
    # Create plot/axis with sizing
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define axis markers and sizes
    ax.set_xticks(x1)
    ax.set_yticks(np.arange(4.0, 6.0, 0.25))
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    
    # Axis labels
    ax.set_xlabel('Months', fontsize="large")
    ax.set_ylabel('Yield (%)', fontsize="large")
    ax.set_title('Interpolated Treasury Par Rates 3/8/24')

    # Scatter points
    plt.scatter(x2,y2, label="Spline Interpolated Par Yields")
    plt.scatter(x3,y3, color="green", marker="s", label='Treasury Par Yields')
    plt.plot(x2, y2)
    
    # Add legend
    plt.legend(loc='upper right', fontsize='large')
    
def spot_rate_curve():
    
    
    


#%%
# Generate plots 
tsy_plot = tsy_rate_plot()
tsy_plot2 = interp_tsy_yld_plot()

#%%




