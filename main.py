import pygame
import math
import json
from dataclasses import dataclass
import sys
import time
import util
WIDTH_SCREEN = 800
HEIGHT_SCREEN = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPASM_CONSTANT = 200
pygame.init()
# CENTRE_SQUARE = (100, 100, 600, 400)
# screen = pygame.display.set_mode([WIDTH_SCREEN, HEIGHT_SCREEN])
# Running = True
# IMAGESCALE = (CENTRE_SQUARE[-2]/3, CENTRE_SQUARE[-1]/3)
# clock = pygame.time.Clock()
# dt = 0
# drawsurface = pygame.Surface((600, 400))
@dataclass
class Rect:
    x:float
    y:float
    width:float
    height:float
    
    def convert(self):
        return (self.x,self.y,self.width,self.height)
    def pos(self):
        return (self.x,round(self.y))
    def size(self):
        return (self.width,self.height)
class Slots:
    def __init__(self,rect:Rect,source:pygame.image,name) -> None:
        self.rect = rect 
        self.source = source
        self.name = name
        self.source = pygame.transform.scale(self.source,self.rect.size())
        self.dy = self.rect.y
    def calculate_pos(self,ds):
        self.rect.y+=ds 
    def render(self,surface:pygame.Surface):
        surface.blit(self.source,self.rect.pos())
class Reel:
    def __init__(self,items:dict) -> None:
        self.items = []
        
        for i,val in enumerate(list(items.items())):
            self.items.append(Slots(Rect(0,1000-i*200,200,200),pygame.image.load(val[1]),name=val[0])) 
    def render(self,surface:pygame.Surface,pt,dt):    
        ds = util.dsmooth_step_by_x(pt,0,3000)*dt
        dss = ds
        # extra iteration in order for it to not spasm away
        # for i in range(int((ds//SPASM_CONSTANT)+1)):       
        #     clamped = util.clamp(0,SPASM_CONSTANT,dss)
        #     print(f"clamped : {clamped}")
        #     for i,item in enumerate(self.items):
        #         # print(i,item.rect.y)
        #         item.calculate_pos(clamped)
        for i, item in enumerate(self.items):
            item.calculate_pos(ds)
        if self.items[0].rect.y>1000:
            t = self.items.pop(0)
            self.items.append(Slots(Rect(0,-200-(1000-t.rect.y),200,200),t.source,name=t.name)) 
        for i in self.items:
            i.render(surface)
class Machine:
    def __init__(self,window_size,main_square,items:dict) -> None:
        self.screen = pygame.display.set_mode(window_size) 
        self.surface= pygame.Surface(main_square)
        self.reel = Reel(items)
        self.items = []
        self.i_count = len(items.keys())
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.t = 10
        self.frame_cap = 1.0/60
        self.time1 = time.perf_counter()
        self.unprocessed = 0
        self.can_render = False
        self.st = 0
        self.t_exe = 0
        self.f_p = 0
    def run_game(self):
        while self.running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if pygame.display.get_init():
                self.can_render = False 
                time_2 = time.perf_counter()
                passed = time_2-self.time1
                self.st+=passed
                self.f_p += passed
                self.unprocessed += passed
                self.time1 = time_2
                while self.unprocessed >= self.frame_cap:
                    self.t_exe+=1 
                    self.surface.fill(WHITE)
                    if self.st <= self.t:
                        self.reel.render(self.surface,self.st/self.t,self.f_p)
                    else:
                        print(self.t_exe)
                        for i,item in enumerate(self.reel.items):
                            print(i,item.rect.y,item.name)
                        sys.exit()
                    # normal setting part
                    self.screen.fill(WHITE)
                    self.screen.blit(self.surface, (100, 100))
                    # done
                    pygame.display.flip()

                    self.unprocessed -= self.frame_cap
                    self.f_p = 0
    # Done! Time to quit.
        pygame.quit()
        sys.exit()
        





def init_with_setting(filename):
    with open(filename) as f:
        data = json.load(f)
    m = Machine(window_size=data["window_size"],main_square=data["main_square"],items=data["items"])
    m.run_game()

init_with_setting("setting.json")
    
