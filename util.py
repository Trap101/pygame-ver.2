def lerp(x1,x2,t):
    return x1+(x2-x1)*t
def smoooth_step(x1,x2,t):
    return x1+(x2-x1)*(t*t*(3-2*t))
def dsmooth_step_by_x(t, cx, dx):
    return cx+(dx-cx)*(6*t-6*t*t)
def clamp(smallest,largest,n):
    return max(smallest,min(n,largest))