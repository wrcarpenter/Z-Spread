import numpy as np

# ticking and unticking bonds for fixed income pricing purposes

def tick(px):
  
    # round eighths to nearest eighth (matches Bloomberg calculations)
    # if negative >> make positive and then add back the negative sign at the end 
  
  sign = 1
  
  if px < 0: 
    px  = abs(px)
    sign = -1
  
  handle  = np.trunc(px)
  decimal = px - handle 
  ticks   = np.trunc(decimal/(1/32))
  eighths = np.round_((decimal/(1/32)-ticks)*8, decimals=0)

  if eighths >= 8:
    ticks   = ticks + 1
    eighths = '' 

  elif eighths == 4:
    eighths = '+'  

  elif eighths == 0: 
    eighths = ''

  else:
    eighths = str('{:0.0f}'.format(eighths))  
  
  if ticks >= 32:
    handle = handle + 1
    ticks = '00'

  elif ticks == 0:
    ticks = '00' 

  elif ticks < 10:
    ticks = '0' + str('{:0.0f}'.format(ticks))

  else:
    ticks = str('{:0.0f}'.format(ticks))

  return str('{:0.0f}'.format(sign*handle) + '-' + ticks + eighths)  


def untick(px):
  
  try:
    x = int(px)
    return px
  
  except:
    print('here')
    index = px.find("-")
    
    if index == -1: 
      return float(px)

    index = px.find("-")
    handle = int(px[:index])
    ticks  = px[index+1:len(px)]

    eights = 0
    
    if len(ticks) == 3: 
      eighths = ticks[-1:]
      ticks   = ticks[:len(ticks)-1]
    
    if eighths == '+': 
      eighths = 4
    print(ticks)
    ticks = int(ticks)/32
    eighths = int(eighths)/8*1/32
    
    return  handle + ticks + eighths 


