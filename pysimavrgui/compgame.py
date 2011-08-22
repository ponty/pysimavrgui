import pygame

class CompositeGame(object):
#    BG_COLOR = 150, 150, 80
    BG_COLOR = 220, 220, 255
    def __init__(self, devs, align=0, size='auto', gap=2):
        self._size = size
        self.devs = devs
        self.align = align
        self.gap = gap
        self._surface = pygame.Surface(self.size)
        
    def update(self):
        self.surface.fill(self.BG_COLOR)     
        pos = [self.gap] * 2
        for x in self.devs:
            x.abs_pos = map(sum, zip(self.abs_pos , pos))
            x.update()
            self.surface.blit(x.surface, pos)
            pos[self.align] += x.size[self.align] + self.gap
            
    def exit(self):
        for x in self.devs:
            if hasattr(x, 'exit'):
                x.exit()
                
    def handleEvents(self, event):
        for x in self.devs:
            if hasattr(x, 'handleEvents'):
                x.handleEvents(event)
            
    @property
    def surface(self):
        return self._surface
    
    @property
    def size(self):
        size = [0, 0]
        devs = self.devs
        sumgap = self.gap * (len(devs) + 1)
        
        i = self.align
        size[i] = sum([d.size[i] for d in devs]) + sumgap
        
        i = 1 - self.align
        size[i] = max([d.size[i] for d in devs]) + 2 * self.gap
        
        return tuple(size)
    
