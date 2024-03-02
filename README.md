# Z-Spread
Z-spread assumes zero volatility in cash flows and interest rates - it is considered to be a "static" valutaion tool, but still more informative than a simple yield spread.

Process:
* Obtain US Treasury par yield data (the assumption of bonds pricing at par is important for calcuations)
* Interpolate yield data using linear or spline-fitting methods
* Derive a zero-coupon curve from CMT data
* Define mortgage bond and mortgage cash flows (cash flows, prepayment speeds, weighted average life)
* Price the bond with Z-spread and J-spread

```math
N = \frac{C}{2} * \frac{N}{1+S}
```



