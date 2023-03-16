import pygame,json,sys,time,util,menu,random
import numpy as np
from dataclasses import dataclass
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
result = {2:{"skull":-100,"else":50},3:{"else":100,"bell":500,"skull":"f"}}
table = {"cherry":0.15,"lemon":0.15,"bell":0.05,"orange":0.15,"star":0.15,"skull":0.35}
t = ["cherry","lemon","star","skull","bell","orange"]
def gen(table:dict):
    value = list(table.keys())
    chance = list(table.values())
    return np.random.choice(value,1,p=chance)
# CENTRE_SQUARE = (100, 100, 600, 400)
# screen = pygame.display.set_mode([WIDTH_SCREEN, HEIGHT_SCREEN])
# Running = True
# IMAGESCALE = (CENTRE_SQUARE[-2]/3, CENTRE_SQUARE[-1]/3)
# clock = pygame.time.Clock()
# dt = 0
# drawsurface = pygame.Surface((600, 400))\

def calculate_offset(current,target,l:list):
    if current not in l or target not in l:
        print(target)
        print(current)
        raise IndexError
    else:
        c_index = l.index(current)
        t_index = l.index(target)
        if t_index >= c_index:
            return t_index-c_index
        elif t_index < c_index:
            return 6-c_index+t_index 
class Slots:
    def __init__(self,rect:pygame.Rect,source:pygame.surface.Surface,name,distance) -> None:
        self.rect = rect 
        self.source = source
        self.name = name
        self.source = pygame.transform.scale(self.source,(self.rect.w,self.rect.h))
        self.s_y = 1000-self.rect.y
        
        self.distance = distance
    def re_init(self,regurgitated_distance):
        self.s_y = self.rect.y+200
        self.distance = regurgitated_distance

    def calculate_pos(self,pt):
        self.rect.y = (util.overease(0,self.distance,pt)+self.s_y)%1200-200
    def reset(self):
        pass
    def render(self,surface:pygame.Surface):
        surface.blit(self.source,(self.rect.x,self.rect.y))
class Reel:
    def __init__(self,items:dict,x,setting=None) -> None:
        self.items = []
        self.x = x
        ## base distance + random
        self.distance = 0
        for i,val in enumerate(list(items.items())):
            self.items.append(Slots(pygame.Rect(x,1000-i*200,200,200),pygame.image.load(val[1]),name=val[0],distance=self.distance))             
        self.re_init()
    def reroll(self):
        result = gen(table)
        print(result)
        offset = calculate_offset(self.c_result(),result,t) 
        self.distance = 7000+offset*200+200
        print(self.distance)
    def re_init(self):
        self.reroll()
        for i in self.items:
            i.re_init(self.distance)
    def c_result(self):
        for i in self.items:
            if i.rect.y == 200:
                return i.name

    def render(self,surface:pygame.Surface,pt):    
        # extra iteration in order for it to not spasm away
        # for i in range(int((ds//SPASM_CONSTANT)+1)):       
        #     clamped = util.clamp(0,SPASM_CONSTANT,dss)
        #     print(f"clamped : {clamped}")
        #     for i,item in enumerate(self.items):
        #         # print(i,item.rect.y)
        #         item.calculate_pos(clamped)
        for i, item in enumerate(self.items):
            item.calculate_pos(pt)
        # if self.items[0].rect.y>=1000:    
        #     t = self.items.pop(0)
        #     s = Slots(Rect(0,-200-(1000-t.rect.y),200,200),t.source,name=t.name,distance=t.distance,trace_distance=t.trace_distance)
        #     s.s_y = t.s_y
        #     self.items.append(s) 
        for i in self.items:
            i.render(surface)
class Machine:
    def __init__(self,setting:dict) -> None:
        items = setting["items"]
        self.items = list(items.keys())
        self.moving = False
        self.screen = pygame.display.set_mode(setting["window_size"]) 
        self.surface= pygame.Surface(setting["main_square"])
        self.reels = [Reel(items,200*(setting["reel_num"]-i-1)) for i in range(setting["reel_num"])]
        self.winning = []
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.t = 5
        self.frame_cap = 1.0/59
        self.time1 = time.perf_counter()
        self.unprocessed = 0
        self.st = 0
        self.f_p = 0
        self.lost = False
        self.button = menu.button(pygame.rect.Rect(775,300,150,100)) 
        for i in self.reels:
            self.button.add_false_event(i.re_init)
        
        self.font = pygame.font.Font("CascadiaMono.ttf",15)
        self.money = 100
        self.button.add_true_event(self.button_press)
    def result(self):
        self.winning = [i.c_result() for i in self.reels]
        f = set(self.winning)
        if len(f) == len(self.winning):
            return
        else:
            dup = {x:self.winning.count(x) for x in self.winning if self.winning.count(x) > 1}
            name = list(dup.keys())[0]
            print(name)
            number = list(dup.values())[0] 
            print(number)
            if number in result:
                if name in result[number]:
                    if result[number][name] == "f":
                        self.lost = True
                    else:
                        self.money += result[number][name]
                else:
                    self.money+=result[number]["else"]
            if self.money <=20:
                self.lost = True
                    
                    

    def button_press(self):
        self.money-=20
    def run_game(self):
        while self.running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if pygame.display.get_init():
                s_font = self.font.render(f"money:{self.money}",True,(0,0,0))
                time_2 = time.perf_counter()
                passed = time_2-self.time1
                self.f_p += passed
                self.unprocessed += passed
                self.time1 = time_2
                if self.button.mouseDown:
                    self.st+= passed
                while self.unprocessed >= self.frame_cap:
                    self.surface.fill(WHITE)
                    if self.st <= self.t:
                        for i,reel in enumerate(self.reels):  
                            reel.render(self.surface,((self.st-i*0.5)/self.t))
                    else:
                        for i, reel in enumerate(self.reels):
                            reel.render(self.surface,1)    
                        self.st = 0
                        self.button.mouseDown = False
                        self.result()
                        
                        
                        
                    # normal setting part
                    self.screen.fill(WHITE) 
                    self.screen.blit(self.surface, (100, 100))
                    self.screen.blit(s_font,(800,100))
                    self.button.render(self.screen,5)
                    # done
                    pygame.display.flip()
                    self.unprocessed -= self.frame_cap
                    self.f_p = 0
    # Done! Time to quit.
        pygame.quit()
        sys.exit()
        





def init_with_setting(filename):
    with open(filename,"r") as f:
        data = json.load(f)
    m = Machine(data)
    m.run_game()
if __name__ == "__main__": 
    init_with_setting("setting.json")
    
