# Z-Spread 

Z-spread assumes zero volatility in cash flows and interest rates - it is considered to be a "static" valutaion tool, but still more informative than a simple yield spread.

# Objectives
Use 'real' Treasury data to calculate zero-coupon rates over a time span of data. 

Create an engine for generating mortgage and corporate bond cash flows with various prepayment assumptions.

Calculate Z-spread for a given cash flow, provided a price, or vice-versa.

# Mathematical Derivation for Zero Coupon Rates

The data provided by the U.S. Treasury gives the yields of bonds at various maturies for a 'par' dollar price. In practice, traders would quote this price as "100-00" and it translates to a 100.00 dollar. The general formula for pricing a par price bond that matures in $n$ periods can written as the following:

```math
P = \frac{\frac{C}{\Delta}*F}{(1+\frac{r_1}{\Delta})^{1}} + \frac{\frac{C}{\Delta}*F}{(1+\frac{r_2}{\Delta})^{2}} + \frac{\frac{C}{\Delta}*F}{(1+\frac{r_3}{\Delta})^{3}} + ... +  \frac{F + \frac{C}{\Delta}*F}{(1+\frac{r_n}{\Delta})^{n}}
```
Where we define:

$P$ -> Price of the bond (assumed to be par or 100.00 given the Treasury rates data)

$C$ -> Annualized coupon of the bond

$\Delta$ -> Compounding period (ex: semiannual bond payments would imply a $\Delta$ of 2)

$F$ -> Face value of the bond (assumed to be 100)

$n$ -> number of periods 

This equation above can be more elegantly written as:

```math
P = \sum_{i=1}^{n-1}\frac{\frac{C}{\Delta}*F}{(1+\frac{r_i}{\Delta})^{i}} +  \frac{F + \frac{C}{\Delta}*F}{(1+\frac{r_n}{\Delta})^{n}}
```







# Procedure
This procedure follows the general methodology for how fixed income analytics providers would calculate zero coupons rates (aka the spot rate curve) with boostrapping and interpolation. 

## Obtain Par-Yield Data
## Interpolate Semi-Annual Par-Yield Rates
## Bootstrap Semi-Annual Zero Coupon Rates
## Interpolate 

# Data Sources

US Treasury Par Yield Rates.

# References



