from entrypoint2 import entrypoint
from path import path
from pysimavr.ac import Ac
from pysimavr.avr import Avr
from pysimavr.connect import connect_pins_by_rule
from pysimavrgui.examples.sim.avrsimmain import AvrSimMain
from pysimavr.firmware import Firmware
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.infogame import InfoGame
from pysimavrgui.lcdgame import LcdGame
from pysimavrgui.ledrowgame import LedRowGame
from pysimavr.lcd import Lcd
from pysimavr.ledrow import LedRow
from pysimavr.vcdfile import VcdFile

@entrypoint
def run_sim(vcdfile='lcd.vcd', speed=0.1, fps=20, timeout=0.0, visible=1, image_file=''):
    firmware = Firmware(path(__file__).dirname() / 'lcd.elf')
    avr = Avr(firmware,f_cpu=16000000)
    lcd = Lcd(avr)
    ledrow = LedRow(avr, size=7)
    # period=1000 -> vcd error
    vcd = VcdFile(avr, period=10, filename=vcdfile)
    
    def state_func(i):
        return (ledrow.pinstate(i), ledrow.reset_dirty(i))
    led_game = LedRowGame(state_func=state_func,
                         labels='D4 D5 D6 D7 RS E RW'.split()  
                         )
    ac = Ac(avr)
    connect_pins_by_rule('''
    avr.B0 <=> lcd.D4 -> vcd
    avr.B1 <=> lcd.D5 -> vcd
    avr.B2 <=> lcd.D6 -> vcd
    avr.B3 <=> lcd.D7 -> vcd
    
    avr.B4 ==> lcd.RS -> vcd
    avr.B5 ==> lcd.E  -> vcd
    avr.B6 ==> lcd.RW -> vcd
    vcd <- ac.OUT -> avr.D2

    lcd.D4 -> led.0
    lcd.D5 -> led.1
    lcd.D6 -> led.2
    lcd.D7 -> led.3
    
    lcd.RS -> led.4
    lcd.E  -> led.5
    lcd.RW -> led.6
                        ''',
                         dict(
                             avr=avr,
                             led=ledrow,
                             lcd=lcd,
                             ac=ac
                             ),
                         vcd=vcd,
                         )
        
    dev = CompositeGame([
                      CompositeGame(
                              [LcdGame(lambda x, y:lcd.get_char(x, y), (20, 2)),
                               led_game,
                               ], 
                                align=1),
                      InfoGame(avr),
                      ])
    
    scrshot_by_exit = [(dev, image_file)] if image_file else None
    
    AvrSimMain(avr, dev, vcd, speed=speed, fps=fps, visible=visible, timeout=timeout,
               scrshot_by_exit=scrshot_by_exit).run_game()

