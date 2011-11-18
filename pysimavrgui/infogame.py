from path import path
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.textgame import TextGame
import pygame
import threading
import time

def format_freq(f):
    if f > 1000000:
        f = f / 1000000.0
        suffix = 'MHz'
    elif f > 1000:
        f = f / 1000.0
        suffix = 'kHz'
    else:
        suffix = 'Hz'
    f = ('%f' % f).rstrip('0').rstrip('.')
    return f + '' + suffix
        
class InfoGame(CompositeGame):
    def __init__(self, avr):
#        firmware = avr.firmware
        cycle_measure_time = 1
        self.speed = 0
        self.start = pygame.time.get_ticks()
        self.firmware_time= '??:??:??'
        self.avr= avr
        
        self.reload()
        
        def avr_state():
            try:
                return avr.states[avr.state]
            except:
                return str(avr.state)
            
        CompositeGame.__init__(self,
                [
                 TextGame((lambda : "mcu=%s" % avr.mcu)),

                 TextGame((lambda : "f_cpu=%s" % format_freq(avr.f_cpu))),
                 TextGame((lambda : "%s (%s)" % (avr.firmware.filename.name
                           ,self.firmware_time))),
                 TextGame((lambda : 'prog: %s bytes %s%% ' % (avr.avrsize.program_bytes, avr.avrsize.program_percentage))),
                 TextGame((lambda : 'mem: %s bytes %s%%' % (avr.avrsize.data_bytes, avr.avrsize.data_percentage))),
                 TextGame((lambda : "vcc=%sV avcc=%sV" % (avr.vcc, avr.avcc))),
                 TextGame((lambda : "pc=%8d" % avr.pc)),
                 TextGame((lambda : "state=%s" % avr_state())),
                 TextGame((lambda : "cycle= %9d" % (avr.cycle))),
                 TextGame((lambda : "mcu time=%s us" % str(1000000 * avr.cycle / avr.f_cpu).rjust(10))),
                 TextGame((lambda : "real time=%s s" % str((pygame.time.get_ticks() - self.start) / 1000).rjust(3))),
                 TextGame((lambda : "real speed= %fx" % (self.speed))),
                 ]
                  , align=1),

        def target():
            c_old = 0
            t_old = 0
            while not self._stop_thread:
                c = avr.cycle
                t = pygame.time.get_ticks()
                
                c_diff = c - c_old
                t_diff = t - t_old
                c_old = c
                t_old = t
                
                if t_diff:
                    self.speed = 1000.0 * c_diff / t_diff / avr.f_cpu
                
                time.sleep(cycle_measure_time)
        
        self._thread = threading.Thread(target=target)
#        self._thread.daemon = 1
        self._stop_thread = False
        self._thread.start()
        
    def reload(self):
        x='??:??:??'
        if self.avr.firmware.filename.exists():
            x = time.strftime("%H:%M:%S", time.localtime(self.avr.firmware.filename.mtime))
        self.firmware_time= x
            
       
        
    def exit(self):
        self._stop_thread = 1
        CompositeGame.exit(self)
       
