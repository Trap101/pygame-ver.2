import math
from dataclasses import dataclass
import pygame
        
@dataclass
class Vector2:
    x:float
    y:float
    
@dataclass
class Rect:
    x:float
    y:float
    width:float
    height:float
    
    def __iter__(self):
        for i in self.__dict__:
            yield self.__dict__[i]
    def convert(self):
        return (self.x,self.y,self.width,self.height)
    def pos(self):
        return (self.x,self.y)
    def size(self):
        return (self.width,self.height)
    def collision_point(self,destination:Vector2):
        return (destination.x > self.x and destination.x < self.x+self.width and destination.y > self.y and self.y <self.y+self.height)
BLACK = (0,0,0)
WHITE= (255,255,255)
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
    """Returns the overshoot ease in and out function
    Parameters:
        pl1 (int):overshoot constant,
        pl2 (int):undershoot constant.
    Returns:
        the returning of a overshoot function.
    """
    return x1+(x2-x1)*(pl1*t*t*(1-t)+(1-(pl2*(1-t))*(pl2*(1-t)))*t)
def overease(x1,x2,t):
    return(x1+(x2-x1)*(1-((1-t)**6)))
def draw_outlined_square(surface,rect:tuple,color:tuple,border_size:int,border_color=None):
    if border_color is None:
        border_color = color
    pygame.draw.rect(surface,color,(800,500,100,100))
    pygame.draw.rect(surface,border_color,rect,border_size)

 