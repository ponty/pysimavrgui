import pygame

class TextGame(pygame.Surface):
    ''' multi line is not supported!'''
    colors = dict(
                text=(0, 0, 0),
#                transparent=(7, 7, 7),
                )
    def __init__(self, text_func, size=(30, 30), font_size=19):
        self._text_func = text_func
        self._size = size
        self.font_size=font_size
        self._font = None
#        self._surface = pygame.Surface(self.size)
#        self.surface.set_colorkey(self.colors['transparent'])
    
    @property
    def size(self):
        return self.font.size(self.text)
    
    @property
    def surface(self):
        text = self.font.render(self.text, 1, self.colors['text'])        
        return text
    
    @property
    def font(self):
        if not self._font:
            pygame.font.init()
            self._font = pygame.font.SysFont("Courier New", self.font_size)
        return self._font

    @property
    def text(self):
        if callable(self._text_func):
            s= self._text_func()
        else:
            s= self._text_func
        # show last line
#        if s:
#            s=s.splitlines()[-1]
        return s
        
     
    def update(self):
#        self.surface.fill(self.colors['transparent'])        
#        text = self.font.render(self.text, 1, self.colors['text'])        
#        self.surface.blit(text, text.get_rect().topleft)
        pass
    
