# Z-Spread 

Z-spread assumes zero volatility in cash flows and interest rates - it is considered to be a "static" valutaion tool, but still more informative than a simple yield spread.

# Objectives
Process:
* Obtain US Treasury par yield data (the assumption of bonds pricing at par is important for calcuations)
* Interpolate yield data using linear or spline-fitting methods
* Derive a zero-coupon curve from CMT data
* Define mortgage bond and mortgage cash flows (cash flows, prepayment speeds, weighted average life)
* Price the bond with Z-spread and J-spread


# Mathematical Derivation for Zero Coupon Yields

```math
N = \frac{C}{2} * \frac{N}{1+S}
```

```math
P_{Bond} = \frac{CF_{1}}{(1+R_1 + Z)^n_1} + \frac{CF_{2}}{(1+R_2 + Z)^n_2} + ... \frac{CF_{i}}{(1+R_i + Z)^n_i}
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



