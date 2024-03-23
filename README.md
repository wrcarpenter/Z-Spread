

# Z-Spread 
> Compound interest is the eighth wonder of the world. He who understands it, earns it ... he who doesn't ... pays it. - Albert Einstein

## Introduction

In fixed income markets, investors rely on various 'spread' measurments to help provide a more informative metric of incremental yield they are receiving vs. a benchmark instrument (ex: Treasury bonds that are often considered to be 'riskless'). This spread would represent compensation for various risks in a given bond that are not in a riskless, benchmark instrument, such as: prepayment risk, credit risk, liquidity risk, etc. Spreads can be readily calculated given a bond cash flow and price and will also give investors a tool to compare relative value between bonds that could have different characteristics. This project focuses on the calculation **Z-Spread**, which assumes *zero-volatility* in cash flows and interest rates - it is considered to be a 'static' valutaion tool, but still more informative than a simple yield spread.

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/zspread-illustration.png)


## Objectives
- Use Treasury data to calculate daily spot rate curves over a given time span 

- Generate mortgage and corporate bond cash flows with various prepayment assumptions

- Calculate Z-spread for a given cash flow, provided a price, or vice-versa

## Procedure
This procedure follows the general methodology for how fixed income analytics providers would calculate zero coupons rates (aka the spot rate curve) with boostrapping and interpolation. 

### Obtain U.S. Treasury Par-Yield Data
To calculate a Z-spread, it is necessary to first source Treasury rate data to construct a spot rate curve from. This raw data can is publically available online here. 

Below is a 3D surface plot of the Treasury data illustrating how the level of rates and shape of the curve each day can flucuate significantly:

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Treasury-Rates-Surface.png)

### Interpolate Semi-Annual Treasury Par-Yield Rates

Given usable rates data, the first step is now to create a interpolated series with semi-annual increments. Practicioners can choose between various spline methods but the two most popular are linear or spline. This project chooses to employ spline interpolation. 

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Interpolated-Treasury-Curve.png)

### Bootstrap Semi-Annual Zero Coupon Rate Curves

![Image](https://github.com/wrcarpenter/Z-Spread/blob/main/Images/Spot-Curve.png)

### Generate a Bond Cash Flow 

Create a mortgage or corporate bond cash flow. Apply varvious prepayment assumptions. 

```Python
def mortgage_cash_flow(settle, cpn, wam, term, balloon, io, delay, speed, prepay_type, bal)
```


### Calculate Z-Spread Given a Bond Price

Take a cashflow and price and determine the yield spread. Apply curve shifts and calculate price sensitivity. Introduce the concept of negative convexity here too. 

### Calcuate Price Given a Bond Z-Spread
 
## Mathematics for Bootstrapping Zero Coupon Rates

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





