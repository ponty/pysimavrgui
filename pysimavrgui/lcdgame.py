from path import path
import logging
import pygame

log = logging.getLogger(__name__)

FONT_SIZE_W = 5
FONT_SIZE_H = 7
FONT_BORDER_W = 1
FONT_BORDER_H = 1

BORDER_W = 10
BORDER_H = 10

SCALE_X = 5
SCALE_Y = 5

class LcdGame(pygame.Surface):
    colors = dict(
                border=(0, 0, 0),
                font_bgr=(120, 240, 120),
                bgr=(100, 240, 100),
                text=(0, 0, 0),
#                transparent=(7, 7, 7),
                )
    def __init__(self, char_func, disp_size=(10, 2) , label=''):
        self.fonts = []
        self.disp_size = disp_size
        self.char_func = char_func
#        self.label = label
        self.disp_size = disp_size
        log.debug('creating surface:' + str(self.size))
        self._surface = pygame.Surface(self.size)
        self.load_fonts()
        
    @property
    def surface(self):
        return self._surface

    @property
    def size(self):
        w = (BORDER_W + self.disp_size[0] * (FONT_SIZE_W + FONT_BORDER_W) * SCALE_X + BORDER_W)
        h = (BORDER_H + self.disp_size[1] * (FONT_SIZE_H + FONT_BORDER_H) * SCALE_Y + BORDER_H)
        return (w, h)

    def load_fonts(self):    
        p=path(__file__).parent / "font.bmp"
        p=p.abspath()
        bmp = pygame.image.load(p);
        bmp.get_rect()
        
        for i in range(255):
            r = pygame.Rect(i * FONT_SIZE_W,
                  0,
                  FONT_SIZE_W,
                  FONT_SIZE_H)
            f = pygame.Surface((r.width, r.height))
            f.blit(bmp, (0, 0), r)
            f = pygame.transform.scale(f, (SCALE_X * FONT_SIZE_W,
                                           SCALE_Y * FONT_SIZE_H))
            f.set_colorkey((255, 255, 255))

            self.fonts += [f]
    
    def update(self):
        self.surface.fill(self.colors['bgr'])        
        pygame.draw.rect(self.surface,
                         self.colors['border'],
                         (0, 0) + self.size,
                         1
                         )   

        for v in range(self.disp_size[1]):
            for i in range(self.disp_size[0]):
                x = BORDER_W + i * (FONT_SIZE_W + FONT_BORDER_W) * SCALE_X;
                y = BORDER_H + v * (FONT_SIZE_H + FONT_BORDER_H) * SCALE_Y;
                w = FONT_SIZE_W * SCALE_X;
                h = FONT_SIZE_H * SCALE_Y;
                index = ord(self.char_func(i, v))
                pygame.draw.rect(self.surface,
                                 self.colors['font_bgr'],
                                 (x, y, w, h)
                                 )   
                f = self.fonts[index]
                self.surface.blit(f, (x, y))

