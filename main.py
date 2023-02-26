import pygame,json,sys,time,util,menu
from dataclasses import dataclass
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.init()
# CENTRE_SQUARE = (100, 100, 600, 400)
# screen = pygame.display.set_mode([WIDTH_SCREEN, HEIGHT_SCREEN])
# Running = True
# IMAGESCALE = (CENTRE_SQUARE[-2]/3, CENTRE_SQUARE[-1]/3)
# clock = pygame.time.Clock()
# dt = 0
# drawsurface = pygame.Surface((600, 400))\
class Slots:
    def __init__(self,rect:pygame.Rect,source:pygame.surface.Surface,name,distance,trace_distance) -> None:
        self.rect = rect 
        self.source = source
        self.name = name
        self.source = pygame.transform.scale(self.source,(self.rect.w,self.rect.h))
        self.s_y = 1000-self.rect.y
        
        self.distance = distance
        self.trace_distance = 0
    def calculate_pos(self,pt):
        self.rect.y = (util.overease(0,8000,pt)+self.s_y)%1200-200
    def reset(self):
        pass
    def render(self,surface:pygame.Surface):
        surface.blit(self.source,(self.rect.x,self.rect.y))
class Reel:
    def __init__(self,items:dict,x) -> None:
        self.items = []
        self.x = x 
        for i,val in enumerate(list(items.items())):
            self.items.append(Slots(pygame.Rect(x,1000-i*200,200,200),pygame.image.load(val[1]),name=val[0],distance=4000,trace_distance=0)) 
    def render(self,surface:pygame.Surface,pt,dt):    
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
        self.moving = False
        self.screen = pygame.display.set_mode(setting["window_size"]) 
        self.surface= pygame.Surface(setting["main_square"])
        self.reels = [Reel(items,200*(setting["reel_num"]-i-1)) for i in range(setting["reel_num"])]
        self.items = []
        self.i_count = len(items.keys())
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.t = 10
        self.frame_cap = 1.0/59
        self.time1 = time.perf_counter()
        self.unprocessed = 0
        self.st = 0
        self.f_p = 0
        self.button = menu.button(pygame.rect.Rect(775,300,150,100))
    def run_game(self):
        while self.running is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if pygame.display.get_init():
                time_2 = time.perf_counter()
                passed = time_2-self.time1
                self.st+=passed
                self.f_p += passed
                self.unprocessed += passed
                self.time1 = time_2
                while self.unprocessed >= self.frame_cap:
                    self.surface.fill(WHITE)
                    if self.st <= self.t:
                        for i,reel in enumerate(self.reels): 
                            pass
                            reel.render(self.surface,self.st/self.t,self.f_p)
                    else:
                        for i, reel in enumerate(self.reels):
                            pass
                            reel.render(self.surface,1,self.f_p)
                    # normal setting part
                    self.screen.fill(WHITE) 
                    self.screen.blit(self.surface, (100, 100))
                    self.button.render(self.screen,5)
                    # pygame.draw.rect(self.screen,BLACK,(800,500,300,300))
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
    
