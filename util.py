import math
def lerp(x1,x2,t):
    return x1+(x2-x1)*t
def smoooth_step(x1,x2,t):
    return x1+(x2-x1)*(t*t*(3-2*t))
def dsmooth_step_by_x(t, cx, dx):
    return cx+(dx-cx)*(6*t-6*t*t)
def clamp(smallest,largest,n):
    return max(smallest,min(n,largest))
def overshoot(x1,x2,t,elastic_constant:int):
    return x1+(x2-x1)*(t*t*elastic_constant*(1-t)+((1-(1-t)*(1-t))*t))
def plastic(x1,x2,t):
    return x1+(x2-x1)*((pow(2,-10*t)*math.sin((10*t-0.75)*2*math.pi/3))+1)
def overshoot_in_out(x1,x2,t,pl1,pl2):
    """easing function
    parameters:
        pl1 :overshoot constantc
        pl2,undershoot constant
    """
    return x1+(x2-x1)*(pl1*t*t*(1-t)+(1-(pl2*(1-t))*(pl2*(1-t)))*t)