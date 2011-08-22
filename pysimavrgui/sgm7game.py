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

SEGMENT_A = (1 << 0)
SEGMENT_B = (1 << 1)
SEGMENT_C = (1 << 2)
SEGMENT_D = (1 << 3)
SEGMENT_E = (1 << 4)
SEGMENT_F = (1 << 5)
SEGMENT_G = (1 << 6)
SEGMENT_P = (1 << 7)
ALL_SEGMENTS = SEGMENT_A | SEGMENT_B | SEGMENT_C | SEGMENT_D | SEGMENT_E | SEGMENT_F | SEGMENT_G | SEGMENT_P

class Sgm7Game(pygame.Surface):
    colors = dict(
                  on=(0, 0, 0),
                off=[230]*3,
                pulse=(222, 0, 0),
                border=(0, 0, 0),
#                sgm_bg=(210, 210, 210),
#                sgm_fg=(255, 0, 0),
                bgr=[210]*3,
                text=(0, 0, 0),
#                transparent=(7, 7, 7),
                )
    def __init__(self, segments_func, disp_size=4 , label=''):
        self.fonts = []
        self.disp_size = disp_size
        self.segments_func = segments_func
#        self.label = label
        log.debug('creating surface:' + str(self.size))
        self._surface = pygame.Surface(self.size)
        
    @property
    def surface(self):
        return self._surface

    @property
    def size(self):
        w = (BORDER_W + self.disp_size * (FONT_SIZE_W + FONT_BORDER_W) * SCALE_X + BORDER_W)
        h = (BORDER_H + (FONT_SIZE_H + FONT_BORDER_H) * SCALE_Y + BORDER_H)
        return (w, h)

    def update(self):
        self.surface.fill(self.colors['bgr'])        
        pygame.draw.rect(self.surface,
                         self.colors['border'],
                         (0, 0) + self.size,
                         1
                         )   
        for i in range(self.disp_size):
            (on,reset)=self.segments_func(i)
            self.draw_digit(i, ALL_SEGMENTS, self.colors['off'])
            self.draw_digit(i, on, self.colors['on'])
            self.draw_digit(i, reset, self.colors['pulse'])

    def draw_digit(self, i, segments, color):
        v = 0
        x = BORDER_W + i * (FONT_SIZE_W + FONT_BORDER_W) * SCALE_X
        y = BORDER_H + v * (FONT_SIZE_H + FONT_BORDER_H) * SCALE_Y
        w = FONT_SIZE_W * SCALE_X
        h = FONT_SIZE_H * SCALE_Y
    
        segm_w = w / 7
        segm_h = w / 7
        edge_w = w / 9
        edge_h = w / 9
    
        x1l = x + edge_w
        x2l = x + w - edge_w - segm_w
        x1r = x1l + segm_w
        x2r = x2l + segm_w
    
        y1t = y + edge_h
        y2t = y + h / 2 - segm_h / 2
        y3t = y + h - edge_h - segm_h
        y1b = y1t + segm_h
        y2b = y2t + segm_h
        y3b = y3t + segm_h
    
        if segments & SEGMENT_P:
            pos = x2r + 1.5 * segm_w, y3t
            r = segm_w
            pygame.draw.circle(self.surface, color, map(int,pos), int(r))   
        
    
        if segments & SEGMENT_E:    
            r = x1l, y2t, x1r - x1l, y3b - y2t
            pygame.draw.rect(self.surface, color, r)   
        
    
        if segments & SEGMENT_C:
            r = x2l, y2t, x2r - x2l, y3b - y2t
            pygame.draw.rect(self.surface, color, r)   
        
    
        if segments & SEGMENT_F:
            r = x1l, y1t, x1r - x1l, y2b - y1t
            pygame.draw.rect(self.surface, color, r) 
        
        if segments & SEGMENT_B:
            r = x2l, y1t, x2r - x2l, y2b - y1t
            pygame.draw.rect(self.surface, color, r) 
        
        if segments & SEGMENT_A:
            r = x1l, y1t, x2r - x1l, y1b - y1t
            pygame.draw.rect(self.surface, color, r) 
        
        if segments & SEGMENT_G:
            r = x1l, y2t, x2r - x1l, y2b - y2t
            pygame.draw.rect(self.surface, color, r) 
        
        if segments & SEGMENT_D:
            r = x1l, y3t, x2r - x1l, y3b - y3t
            pygame.draw.rect(self.surface, color, r) 
        

