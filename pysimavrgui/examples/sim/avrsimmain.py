from pysimavrgui.maingame import MainGame
import logging

log = logging.getLogger(__name__)

class AvrSimMain(MainGame):
    def __init__(self, avr, dev, vcd, timeout=None, visible=1, speed=1, fps=20, scrshot_by_exit=None):
        log.debug('visible=%s timeout=%s speed=%s'%(visible, timeout,speed))
        self.avr = avr
        self.vcd = vcd
        self.speed = speed
        self.timeout = timeout            
        MainGame.__init__(self, dev, fps=fps, visible=visible, scrshot_by_exit=scrshot_by_exit)
        
    def run_game(self):
        if self.vcd:
            self.vcd.start()
        MainGame.run_game(self)
            
    def cb_loop(self):
        ''
        self.avr.move_time_marker(1.0 * float(self.speed) / self.fps)
        if self.timeout:
#            self.avr.goto_time(self.timeout)
            if self.avr.time_passed() >= self.timeout:
                log.debug('avr.time_passed=%d' % self.avr.time_passed())
                log.debug('timeout=%d' % self.timeout)
                log.debug('exiting')
                self.exit = True               
            
    def cb_exit(self):
        if self.vcd:
            self.vcd.terminate()
        self.avr.terminate()



