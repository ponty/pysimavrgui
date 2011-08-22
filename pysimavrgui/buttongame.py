import pygame
#import pygame.gfxdraw

class ButtonGame(pygame.Surface):
    colors = dict(
                  on=(255, 100, 100),
                off=(100, 255, 100),
                border=(0, 0, 0),
                text=(0, 0, 0),
                transparent=(7, 7, 7),
                )
    def __init__(self, hook=None, shortcut=None, label='', size='auto', display_shortcut=True, font_size=14):
        self.label = label
        if display_shortcut and shortcut:
            self.label += ' (%s)' % shortcut
        self.font_size = font_size
        self.shortcut = shortcut
        self.hook = hook if hook else dict()
        self.pressed = False
        self._size = size
        pygame.font.init()
        self.font = pygame.font.SysFont("Courier New", self.font_size)
        if size == 'auto':
            self._size = self.font.size(self.label)  
            self._size=(self._size[0]+10,self._size[1]+5)     
        self._surface = pygame.Surface(self.size)
        self.key = None

#        self.font = None
        self._bg = self._surface.copy()
        self._bg.fill(self.colors['transparent'])     
        self.surface.set_colorkey(self.colors['transparent'])
        
         
        edge = 2
        self.center = (self.size[0] / 2, self.size[1] / 2)
        self.rect = pygame.Rect(edge, edge, self.size[0] - edge, self.size[1] - edge)
    
    @property
    def size(self):
        return self._size
    
    @property
    def surface(self):
        return self._surface
        
    def update(self):
#        if not self.font:
        self.surface.blit(self._bg, (0, 0))
        if self.pressed:
            color = self.colors['on']
        else:
            color = self.colors['off']
        pygame.draw.rect(self.surface, color, self.rect, 0)
        pygame.draw.rect(self.surface, self.colors['border'], self.rect, 1)
        if self.label:
            text = self.font.render(self.label, 1, self.colors['text'])        
            self.surface.blit(text, text.get_rect(center=self.center).topleft)
            
    def _press(self, b):
        self.pressed = b
        f = self.hook.get('down' if b else 'up')
        if f:
            f()
            
    def handleEvents(self, event):
        abs_rect = self.rect.move(*self.abs_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs_rect.collidepoint(event.pos) and event.button == 1:
                self._press(True)
        if event.type == pygame.MOUSEBUTTONUP:
            if abs_rect.collidepoint(event.pos) and event.button == 1:
                self._press(False)
        if event.type == pygame.KEYDOWN:
            if event.unicode == self.shortcut:
                self.key = event.key
                self._press(True)
        if event.type == pygame.KEYUP:
            if event.key == self.key:
                self._press(False)
