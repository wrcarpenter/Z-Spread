"""
Z-Spread Charting

Code for charts used in the 'Z-Spread' project. 

Author: Will Carpenter

"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, MaxNLocator
# Additioanl imports for charting
from matplotlib.colors import LightSource
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.dates import DateFormatter

#%%
# Read in par-yield data
tsy   = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-rates.csv", header=0)
head  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/daily-treasury-spot-header.csv")
spots = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/spots-semi-annual.csv", header=0)
ylds  = pd.read_csv("https://raw.githubusercontent.com/wrcarpenter/Z-Spread/main/Data/ylds-semi-annual.csv", header=0)

# Define columns 
tsy_cols = list(tsy.columns.values)
cols     = list(head.columns.values)

#%%
from matplotlib.colors import LightSource
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.dates import DateFormatter

def tsy_rate_plot():
    
    # Define data
    x1 = np.array(tsy_cols[5:])
    x1 = x1.astype(float)
    y1 = np.array(tsy.loc[1])
    y1 = y1[5:]
    # Define figure
    fig, ax = plt.subplots(figsize=(11, 5))
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
    x2 = np.array(list(ylds.columns.values[2:])).astype(float)
    y2 = np.array(ylds.loc[1])
    y2 = y2[2:]
    
    # Define data 
    x3 = np.array(tsy_cols[5:])
    x3 = x3.astype(float)
    y3 = np.array(tsy.loc[1])
    y3 = y3[5:]
    
    # Create plot/axis with sizing
    fig, ax = plt.subplots(figsize=(11, 5))
    
    fig.patch.set_facecolor('gainsboro')
    
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
    plt.scatter(x3,y3, color="darkgreen", marker="s", label='Treasury Par Yields')
    plt.plot(x2, y2)
    
    # Add legend
    plt.legend(loc='upper right', fontsize='large')
    
def spot_rate_curve():
    
    x1 = np.array(tsy_cols[5:])
    x1 = x1.astype(float)
    x2 = np.array(list(ylds.columns.values))
    x2 = x2[2:].astype(float)
    y2 = np.array(ylds.loc[1])
    y2 = y2[2:]
    
    y3 = np.array(spots.loc[1])
    y3 = y3[2:]
    
    fig, ax = plt.subplots(figsize=(11, 5))
    
    # Background plot color
    fig.patch.set_facecolor('gainsboro')
    
    ax.set_xticks(x1)
    ax.set_yticks(np.arange(4.0, 6.0, 0.5))
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    
    # Axis labels
    ax.set_xlabel('Months', fontsize="large")
    ax.set_ylabel('Yield (%)', fontsize="large")
    ax.set_title('Spot and Yield Rates 3/8/24')
    
    # Scatter plots
    plt.scatter(x2,y2, label="Spline Interpolated Par Yields")
    plt.scatter(x2,y3, color="darkblue", label='Spot Rates')
    
    # Line plots
    plt.plot(x2, y2)
    plt.plot(x2, y3, color="darkblue")
    
    # Adding legend
    plt.legend(loc='upper right', fontsize='large')
    
#def z_spread_visual():
    # use the arrow function in matplotlib 


def tsy_rate_surface(elevation, azimuthal):
    
    tsy['Date'] = pd.to_datetime(tsy['Date'], format='%m/%d/%Y')
       
    z = tsy.iloc[: , 1:].to_numpy()  # numpy list
    x = tsy['Date'].to_numpy().astype('datetime64[D]')
    
    
    x = x.astype(float)
    #x = np.array(x, dtype='datetime64')
    y = np.array(list(tsy.columns.values[1:])).astype(float)  # tenors
    
    #t1 = pd.DataFrame(Z)
    #t1.to_clipboard()    
    
    X, Y = np.meshgrid(x, y)
    Z = z.T
    
    fig = plt.figure(figsize=(12, 15))
    ax = fig.add_subplot(111, projection='3d')
    
    start_date = min(x)
    end_date = max(x)
    
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%d'))  # Define date format
    
    # ax.set_box_aspect([2, 1, 1])
    
    rts    = np.arange(2.0, 6.0, 0.5)
    tenors = np.arange(0, 400, 60)
    
    ax.set_yticks(tenors)
    ax.set_zticks(rts)
    
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    
    ax.view_init(elev=elevation, azim=azimuthal)    #40,50    40,110   to flip around
    
    
    ax.set_xlabel('Date', labelpad=20)
    ax.set_ylabel('Tenor (months)', labelpad=20)
    ax.set_zlabel('Rate (%)', labelpad=3)
    ax.set_title('Treasury Par Yields Overtime', fontsize='large')
    
    surf = ax.plot_surface(X,Y,Z, cmap='plasma',
                       linewidth=0, antialiased=False)

#%%
# Generate plots 
tsy_rates  = tsy_rate_plot()
tsy_interp = interp_tsy_yld_plot()
spot_curve = spot_rate_curve()
surf1      = tsy_rate_surface(40, 50)
surf2      = tsy_rate_surface(40, 110)

