"""
Unit Testing Z-Spread
Author: W. Carpenter
"""

#%%
# Unit Testing mortgage cash flows 
# Returns an array with mortgage cash flows

# cash flows at different prepayment speeds
cf_0cpr  = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 45,  0, 'CPR', 500000)
cf_5cpr  = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 45,  5, 'CPR', 500000)
cf_20cpr = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 45, 25, 'CPR', 500000)
cf_40cpr = mortgage_cash_flow('03/01/2024', 7.00, 360, 360, 360, 0, 45, 40, 'CPR', 500000)

#%%
# Unit testing for mortgage average life


