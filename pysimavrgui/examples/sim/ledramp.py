from entrypoint2 import entrypoint
from path import path
from pysimavr.avr import Avr
from pysimavr.connect import connect_pins_by_rule
from pysimavrgui.examples.sim.avrsimmain import AvrSimMain
from pysimavr.firmware import Firmware
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.infogame import InfoGame
from pysimavrgui.ledrowgame import LedRowGame
from pysimavr.ledrow import LedRow
from pysimavr.vcdfile import VcdFile

@entrypoint
def run_sim(vcdfile='ledramp.vcd', speed=0.1, fps=20, timeout=0.0, visible=1, image_file=''):
    firmware = Firmware(path(__file__).dirname() / 'ledramp.elf')
    avr = Avr(firmware, f_cpu=8000000, mcu='atmega48')

    vcd = VcdFile(avr, period=1000, filename=vcdfile)
    ledrow = LedRow(avr)
    connect_pins_by_rule('''
                        avr.B0 ==> led.0 -> vcd
                        avr.B1 ==> led.1 -> vcd
                        avr.B2 ==> led.2 -> vcd
                        avr.B3 ==> led.3 -> vcd
                        avr.B4 ==> led.4 -> vcd
                        avr.B5 ==> led.5 -> vcd
                        avr.B6 ==> led.6 -> vcd
                        avr.B7 ==> led.7 -> vcd
                        ''',
                         dict(
                             avr=avr,
                             led=ledrow,
                             ),
                         vcd=vcd,
    )
    
    def state_func(i):
        return (ledrow.pinstate(i), ledrow.reset_dirty(i))
    led_game = LedRowGame(state_func=state_func,
                          labels=['B' + str(x) for x in range(8)])
        
    dev = CompositeGame([
                        led_game,
                        InfoGame(avr),
                        ])
    
    scrshot_by_exit = [(dev, image_file)] if image_file else None

    AvrSimMain(avr, dev, vcd, speed=speed, fps=fps, visible=visible, timeout=timeout,
               scrshot_by_exit=scrshot_by_exit).run_game()
