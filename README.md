

# Z-Spread 
> Compound interest is the eighth wonder of the world. He who understands it, earns it ... he who doesn't ... pays it. - Albert Einstein

Go directly to the code files:
| Type | Code | Description | 
| --- | --- | --- |
| Z-Spread | [Here](https://github.com/wrcarpenter/Z-Spread/blob/main/z_spread.py) | Method to calculate a bond's Z-spread. Also implements pricing with I-spread and calculating Macaulay duration. |
| Spot Rate Bootstrap | [Here](https://github.com/wrcarpenter/Z-Spread/blob/main/spot_rate_bootstrap.py) | Process to take Treasury data and boostrap a spot rate curve (described in more detail below).|
| Mortgage Cash Flows | [Here](https://github.com/wrcarpenter/Z-Spread/blob/main/mortgage_cash_flow.py)| Cash flow engine written in Python. Generates monthly mortgage cash flows at various prepayment speeds. Can also calculate a mortgage's Weighted Average Life (WAL).| 

## Table of Contents
[Introduction](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#introduction)

[Objectives](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#objectives)

[Procedure](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#procedure)
* [Obtain US Treasury Par Yield Data](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#obtain-us-treasury-par-yield-data)
* [Interpolate Semi-Annual Par Yields](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#obtain-us-treasury-par-yield-data)
* [Boostrap Semi-Annual Zero Coupon Rates](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#bootstrap-semi-annual-zero-coupon-rate-curves)
* [Generate a Bond Cash Flow](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#generate-a-bond-cash-flow)
* [Calculate a Bond's Z-Spread](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#calculate-z-spread-given-a-bond-price)

[Bootstrapping Mathematics](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#mathematics-for-bootstrapping-zero-coupon-rates)

## Introduction

In fixed income markets, investors rely on various 'spread' measurments to help provide a more informative metric of incremental yield they are receiving vs. a benchmark instrument (ex: Treasury bonds that are often considered to be 'riskless'). This spread would represent compensation for various risks in a given bond that are not in a riskless, benchmark instrument, such as: prepayment risk, credit risk, liquidity risk, etc. Spreads can be readily calculated given a bond cash flow and price and will also give investors a tool to compare relative value between bonds that could have different characteristics. This project focuses on the calculation **Z-Spread**, which assumes *zero-volatility* in cash flows and interest rates - it is considered to be a 'static' valutaion tool, but still more informative than a simple yield spread.

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/zspread-illustration.png)



## Objectives
- Use Treasury data to calculate daily spot rate curves over a given time span 

- Generate mortgage and corporate bond cash flows with various prepayment assumptions

- Calculate Z-spread for a given cash flow, provided a price, or vice-versa

## Procedure
This procedure follows the general methodology for how fixed income analytics providers would calculate zero coupons rates (aka the spot rate curve) with boostrapping and interpolation. 

## Obtain U.S. Treasury Par-Yield Data
To calculate a Z-spread, it is necessary to first source Treasury rate data to construct a spot rate curve from. This raw data can is publically available online [here](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2024).

Below is a 3D surface plot of the Treasury data illustrating how the level of rates and shape of the curve each day can flucuate significantly:

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Treasury-Rates-Surface.png)

## Interpolate Semi-Annual Treasury Par-Yield Rates

Given usable rates data, the first step is now to create a interpolated series with semi-annual increments. Practicioners can choose between various spline methods but the two most popular are linear or spline. This project employs spline interpolation.

```Python
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
```
Below is a chart that illustrates how spline interpolation compares to given Treasury Par Yields (marked as the green squares). This specifc curve is created from Treasury data on March 8th, 2024 where one can see the front-end is sharply inverted.

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Interpolated-Treasury-Curve.png)

## Bootstrap Semi-Annual Zero Coupon Rate Curves

With semi-annual Treasury data, the next step is to perform a bootstrapping methodology to iterively solve for zero coupon yields. 

```Python
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

```


![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Spot-Curve.png)

## Generate a Bond Cash Flow 

This project has a mortgage cash flow engine that can handle different payment delays, settle dates, and prepayment rate assumptions.  

```Python
def mortgage_cash_flow(settle, cpn, wam, term, balloon, io, delay, speed, prepay_type, bal) -> pd.DataFrame:

# returns pd dataframe with monthly mortgage cash flows
# prepay_type is currently 'CPR' which is a conditional prepayment rate that can be converted to an SMM 

```

### Calculate Z-Spread Given a Bond Price

Take a cashflow and price and determine the yield spread. Apply curve shifts and calculate price sensitivity. Introduce the concept of negative convexity here too. 

### Calcuate Price Given a Bond Z-Spread
 
## Mathematical Background

### Bootstrapping Zero Coupon Rates

The following sections cover the mathematics behind Tresaury bond pricing and how to utlize market data to boostrap a spot rate curve. These calculations are all implemented in the code for this project.

The data provided by the U.S. Treasury gives the yields of bonds at various maturies for a 'par' dollar price. In practice, traders would quote this price as "100-00" and it translates to a 100.00 dollar. The general formula for pricing a par price bond that matures in $n$ periods can written as the following:

```math
P = \frac{\frac{C}{\Delta}*F}{(1+\frac{r_1}{\Delta})^{1}} + \frac{\frac{C}{\Delta}*F}{(1+\frac{r_2}{\Delta})^{2}} + \frac{\frac{C}{\Delta}*F}{(1+\frac{r_3}{\Delta})^{3}} + ... +  \frac{F + \frac{C}{\Delta}*F}{(1+\frac{r_n}{\Delta})^{n}}
```
Where we define:

* $P$ : Price of the bond (assumed to be par or 100.00 given the Treasury rates data)

* $C$ : Annualized coupon of the bond

* $\Delta$ : Compounding period (ex: semiannual bond payments would imply a $\Delta$ of 2)

* $F$ : Face value of the bond (assumed to be 100)

* $n$ : number of periods 

This equation above can be more elegantly written as:

```math
P = \sum_{i=1}^{n-1}\frac{\frac{C}{\Delta}*F}{(1+\frac{r_i}{\Delta})^{i}} +  \frac{F + \frac{C}{\Delta}*F}{(1+\frac{r_n}{\Delta})^{n}}
```
This equation is quintessential example of discounted cashflow pricing, which is the foundation for the bond market and illustrates the concept of 'present value.' Diving into the cashflows first, one can see thatin each period before the bond matures at time $n$ a bond holder would receive an intermediate interest payment of $\frac{C}{\Delta}*F$ which adjusts the coupon if the payments are not necessarily annual. In the case of Treasury bonds, payments are semi-annual.





