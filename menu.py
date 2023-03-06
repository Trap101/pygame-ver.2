import pygame
import util

class button:
    def __init__(self,rect:pygame.rect.Rect,mouseDown = False) -> None:
        self.rect = rect
        self.outline = util.WHITE
        self.background = util.BLACK
        self.false_event = util.Event()
        self.true_event = util.Event()
        self.mouseDown = False

    @property
    def mouseDown(self):
        return self._mouseDown
    @mouseDown.setter
    def mouseDown(self,rhs:bool):
        if rhs == False:
            self.false_event()
        if rhs == True:
            self.true_event()
        self._mouseDown = rhs
            
    def render(self,surface,border_size):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint((pos[0],pos[1])):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == True and self.mouseDown != True:
                self.mouseDown = True
            self.outline = util.BLACK
            self.background = util.WHITE 
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.outline = util.WHITE
            self.background = util.BLACK
        pygame.draw.rect(surface,self.background,self.rect)
        pygame.draw.rect(surface,self.outline,self.rect,border_size)
        pygame.draw.rect(surface,util.BLACK,pygame.rect.Rect(self.rect.x,self.rect.y,self.rect.width,self.rect.height),border_size)
    def add_false_event(self,objmethod):
        self.false_event+=objmethod
    
    def remove_false_event(self,objmethod):
        self.false_event -= objmethod
    def add_true_event(self,objmethod):
        self.true_event+=objmethod
    def remove_true_event(self,objmethod):
        self.true_event -= objmethod
    
        
    
    
        
        
    
        