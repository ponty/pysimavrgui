from path import path
import logging
import pygame

log = logging.getLogger(__name__)

class MainGame(object):
#    BG_COLOR = 150, 150, 80
    BG_COLOR = 100, 100, 180
    def __init__(self, dev, pos=(0, 0), fps=50, size='auto', title='python-simavr', visible=True, scrshot_by_exit=None):
        self.scrshot_by_exit = scrshot_by_exit
        self.visible = visible
        self.fps = fps
        self.size = size
        self.dev = dev
        self.pos = pos
        self.title = title
        self.exit = False               
        self.exception = None
               
    def cb_loop(self):
        pass
    
    def cb_exit(self):
        pass
    
    def screenshot(self, dev=None, img_file='screenshot.png'):
        if not dev:
            dev = self.dev
        img_file = path(img_file).abspath()
        log.debug('saving ' + str(img_file))
        pygame.image.save(dev.surface, img_file)

    def run_game(self):
        pygame.init() 
        if self.visible:
            pygame.display.set_caption(self.title) 
        clock = pygame.time.Clock()
        if self.size == 'auto':
            size = self.dev.size
            
        if self.visible:
            #create the screen
            self.window = pygame.display.set_mode(size, 0)
        else:  
            self.window = pygame.Surface(size)

        
        log.debug('driver:' + pygame.display.get_driver())
        while not self.exit:
            # Redraw the background
            self.window.fill(self.BG_COLOR)     
            
            self.dev.abs_pos = self.pos
            self.dev.update()            
            self.window.blit(self.dev.surface, self.pos)
            
            if self.visible:            
                #draw it to the screen
                pygame.display.flip()
    
    
            # Limit frame speed
            self.time_passed = clock.tick(self.fps) 
            real_fps = (clock.get_fps())
            pygame.display.set_caption(
                      '{title} (fps={real_fps})'.format(
                                        title=self.title,
                                        real_fps=int(0.5 + real_fps)))

            self.cb_loop()
            try:
                self.handleEvents()
            except Exception as e:
                self.exception = e
                break    
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:                    
#                    self.exit = True
        self.terminate()
        
    def handleEvents(self):
        exit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                    
                self.exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit = True
            if hasattr(self.dev, 'handleEvents'):
                self.dev.handleEvents(event)
        
    def terminate(self):   
        if self.scrshot_by_exit:
            for dev, img_file in self.scrshot_by_exit:
                self.screenshot(dev, img_file)
        self.cb_exit()
        if hasattr(self.dev, 'exit'):
            self.dev.exit()
#        pygame.quit()
#        sys.exit()
        if                 self.exception:
            raise                 self.exception 




