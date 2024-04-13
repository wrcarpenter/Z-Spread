

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

[Fixed Income Mathematics Background](https://github.com/wrcarpenter/Z-Spread?tab=readme-ov-file#mathematics-for-bootstrapping-zero-coupon-rates)

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

With semi-annual Treasury data, the next step is to perform a bootstrapping methodology to iterively solve for zero coupon yields. The bond market does not provide available pricing for zero coupon bond for every month in the future for the next 20-30 years, but it is possible to infer from actively traded Treasuries. For Z-spread pricing purposes, it is important to have zero coupon bond yields rather than Treasuries because a Treasury bonds yield factors in semi-annual interest payments. For a singular cash flow in a given month $X$, the discount factor for that cashflow must also only have one payment for that month for an accurate "apples-to-apples" comparision.  

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
Employing the methodology above, a spot rate curve can be created for every daily Treasury curve provided in the data. See chart below for one example of overlaying the par yield and spot curve on March 8th, 2024. 

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Spot-Curve.png)

## Generate a Bond Cash Flow 

This project focuses on mortgage pricing and has its own mortgage cash flow engine that can handle different payment delays, settle dates, and prepayment rate assumptions.  

```Python
def mortgage_cash_flow(settle, cpn, wam, term, balloon, io, delay, speed, prepay_type, bal) -> pd.DataFrame:

# returns pd dataframe with monthly mortgage cash flows
# prepay_type is currently 'CPR' which is a conditional prepayment rate that can be converted to an SMM 

```
One example of a cashflow input could be the following:

```Python
cf_7cpr = mbs.cash_flow('03/29/2024', 6.50, 360, 360, 240, 0, 54,  7, 'CPR', 1000000)
```
This is a $1,000,000 bond with a 6.5% coupon, 20-year balloon maturity, and 30-year amortization schedule. It is also assumed to prepay monthly principal at a rate of '7 CPR' which is where the variable naming comes from as well. Once this cash flow is created it is also possible to calculate its WAL (Weighted Average Life) which is important to have when determining a bond's yield when given a Z-Spread or I-Spread. The following code is used in this project to calculate WAL:

```Python
def wal(settle, cf) -> float:
    
    '''
    Calculate weighted-average-life of a mortgage cash flow.
    '''
    arr = cf
    
    settle       = pd.to_datetime(settle, format="%m/%d/%Y")
    arr['settle'] = settle
    arr['diff']   = (pd.to_datetime(arr['Date']) - arr['settle']).dt.days
    
    num          = (arr['diff']*((arr['Scheduled Principal'] + arr['Unscheduled Principal']))).sum()
    denom        = (arr['Scheduled Principal'] + arr['Unscheduled Principal']).sum()          
    wal          = num/denom*1/365
         
    return wal
```

## Calculate Price Given a Bond Z-Spread

Given a defined security cashflow and spread, it is possible to calculate a yield and Z-spread for the security. The following is the pricing engine that can calculate both Z-Spread and I-spread:

``` Python
def price(cf, curve, settle, spread, typ) -> float:

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
```
In order for the pricing engine to function above, a monthly equivalent yield (MEY) must be calculated that involves first calculating a bond's weighted average life and interpolating a yield at that point. Below is the helper function for MEY that assists the pricing engine:

```Python

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

```

## Calculate Z-Spread Given a Bond Price

Calculating spread given a bond price involves using the pricing engine with a root finding algorithm. In short, the function given is $Solver - Price = 0$ where the $Price$ is given and the $Solver$ is the pricing function that iteraively tests different spread values until the fucntion finally equals zero. The following is the code that employs this method using the projects pricing engine:

```Python
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
```
While this project focuses primarily on Z-Spread and the methodology behind it, the code above can also solve for I-Spread ('interpolated' yield spread). 
 
## Mathematical Background

For those interested, the final part of this project provides an overview of the fixed income mathematics used for calculations in the code.

## Bootstrapping Zero Coupon Rates

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

## Solving for a Mortgage Bond Price





