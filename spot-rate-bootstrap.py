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

#%%
# Saving down relevant data (local drive) 

ylds.to_csv('C:/Users/wcarp/OneDrive/Desktop/Z-Spread/Data/ylds-semi-annual.csv')
spots.to_csv('C:/Users/wcarp/OneDrive/Desktop/Z-Spread/Data/spots-semi-annual.csv')

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

spots_monthly = pd.DataFrame(np.delete(ylds, 0, 0))        

# spots_monthly.to_clipboard()
#%% Plotting (creating custom project plots)

# Plot treasury points

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

def spot_rate_visual():
    
    x1 = np.array(tsy_cols[5:])
    x1 = x1.astype(float)
    x2 = np.array(list(ylds.columns.values))
    x2 = x2[2:].astype(float)
    
    y3 = np.array(spots.loc[1])
    y3 = y3[2:]
    
    y4 = np.add(y3, 0.70)
    
    
    
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
    plt.scatter(x2,y3, color="darkblue", label='Spot Rates')
    plt.scatter(x2, y4, color="blue", marker='x')
    
    # Line plots
    plt.plot(x2, y3, color="darkblue")
    
    for pt in y4:
        plt.plot(np.array(x2[pt], x2[pt]), np.array(y4[pt], y4[pt]), color="blue")
    
    # Adding legend
    plt.legend(loc='upper right', fontsize='large')
    

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
plot1 = tsy_rate_plot()
plot2 = interp_tsy_yld_plot()

#%%
plot3 = spot_rate_curve()

#%%
plot4 = tsy_rate_surface(40, 50)
plot5 = tsy_rate_surface(40, 110)

#%%
plot6 = spot_rate_visual()


x1 = np.array(tsy_cols[5:])
x1 = x1.astype(float)
x2 = np.array(list(ylds.columns.values))
x2 = x2[2:].astype(float)

y3 = np.array(spots.loc[1])
y3 = y3[2:]

y4 = np.add(y3, 0.70)

fig, ax = plt.subplots(figsize=(14, 4))

# Background plot color
fig.patch.set_facecolor('white')

ax.set_xticks(x1)
ax.set_yticks(np.arange(4.0, 6.0, 0.5))
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# Axis labels
ax.set_xlabel('Months', fontsize="large")
ax.set_ylabel('Yield (%)', fontsize="large")
ax.set_title('Calculating Z-Spread: An Illustration')


for pt in range(0,len(y4)):

    linex = np.array([x2[pt], x2[pt]])
    liney = np.array([y3[pt], y4[pt]])
    
    plt.plot(linex, liney, color="lightblue",linewidth=2,linestyle='dashed')

# Adding legend


# Line plots
plt.plot(x2, y3, color="darkblue")
plt.plot(x2, y3, color="darkblue")

# Scatter plots
plt.scatter(x2,y3, color="darkblue", label='Spot Rates')
plt.scatter(x2, y4, color="blue", marker='x', label='Spot Yields' )

plt.legend(loc='upper right', fontsize='large')








