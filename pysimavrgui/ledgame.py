import pygame
import pygame.gfxdraw

class LedGame(pygame.Surface):
    colors = dict(
                  on=(255, 100, 100),
                off=(100, 255, 100),
                pulse=(175, 175, 100),
                border=(0, 0, 0),
                text=(0, 0, 0),
                transparent=(7, 7, 7),
                )
    def __init__(self, state_func, label='', size=(30, 30)):
        self._state_func = state_func
        self.label = label
        self._size = size
        self._surface = pygame.Surface(size)
        edge = 2
        self.pos = (self.size[0] / 2, self.size[1] / 2)
        self.r = min(self.size) / 2 - edge
        self.font = None
        self._bg=self._surface.copy()
#        self._bg.set_alpha(1)
        self._bg.fill(self.colors['transparent'])     
#        self._bg.set_colorkey(self.colors['transparent'])
        self.surface.set_colorkey(self.colors['transparent'])
    
    @property
    def size(self):
        return self._size
    
    @property
    def surface(self):
        return self._surface

    @property
    def state(self):
        ' (on/off,pulse)'
        if callable(self._state_func):
            return self._state_func()
        else:
            return self._state_func
        
    @property
    def on(self):
        return self.state[0]

    @property
    def pulse(self):
        return self.state[1]
    
    def update(self):
        if not self.font:
            self.font = pygame.font.SysFont("Courier New", self.r)
#        self.surface.fill(self.colors['transparent'])     
        self.surface.blit(self._bg, (0,0))
   
#        pygame.draw.circle(self.surface,
#                           self.colors[self.state],
#                           self.pos,
#                           self.r,
#                           )
        if self.pulse:
            color=self.colors['pulse']
        elif self.on:
            color=self.colors['on']
        else:
            color=self.colors['off']
        pygame.gfxdraw.filled_circle(self.surface,
                                     self.pos[0], self.pos[1], self.r ,
                                     color)
        if self.label:
            text = self.font.render(self.label, 1, self.colors['text'])        
            self.surface.blit(text, text.get_rect(center=self.pos).topleft)
        pygame.gfxdraw.aacircle(self.surface,
                                     self.pos[0], self.pos[1], self.r ,
                                     self.colors['border'])
    
