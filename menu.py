import pygame
import util

class button:
    def __init__(self,rect:pygame.rect.Rect) -> None:
        self.rect = rect
        self.outline = util.WHITE
        self.background = util.BLACK
        self.mouse_down = False
    def render(self,surface,border_size):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint((pos[0],pos[1])):
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == True:
                self.mouse_down = True
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
    
    
        
        
    
        