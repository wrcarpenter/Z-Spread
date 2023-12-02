# Z-Spread
Creating a zero coupon rates curve and calculating Z-spread for fixed income bonds. 

Z-spread assumes zero volatility in cash flows and interest rates - it is considered to be a "static" valutaion tool, but still more informative than a simple yield spread.

Process:
* Derive a zero-coupon curve from CMT data
* Define mortgage bond and mortgage cash flows (cash flows, prepayment speeds, weighted average life)
* Price the bond with Z-spread and J-spread 
