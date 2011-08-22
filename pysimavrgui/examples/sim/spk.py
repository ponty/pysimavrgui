from entrypoint2 import entrypoint
from path import path
from pysimavr.ac import Ac
from pysimavr.avr import Avr
from pysimavr.connect import connect_pins_by_rule
from pysimavr.firmware import Firmware
from pysimavr.ledrow import LedRow
from pysimavr.spk import Spk
from pysimavr.vcdfile import VcdFile
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.examples.sim.avrsimmain import AvrSimMain
from pysimavrgui.infogame import InfoGame
from pysimavrgui.ledrowgame import LedRowGame
from pysimavrgui.spkgame import SpkGame

@entrypoint
def run_sim(vcdfile='spk.vcd', speed=0.5, fps=20, timeout=0.0, visible=1, image_file='',rate=11025):
    firmware = Firmware(path(__file__).dirname() / 'spk.elf')
    avr = Avr(firmware=firmware,
              mcu="atmega168",
              f_cpu=16000000,
              )
    ledrow = LedRow(avr, size=1)
    # period=1000 -> vcd error
    vcd = VcdFile(avr, period=10, filename=vcdfile)
    spk = Spk(avr, rate=rate, speed=speed)
    
    connect_pins_by_rule('''
    led.0 <-- avr.B5 --> spk.IN -> vcd
                        ''',
                         dict(
                             avr=avr,
                             spk=spk,
                             led=ledrow,
                             ),
                         vcd=vcd,)
    ####################################                     )
    # GUI        
    def spk_func(size):
        return spk.read()
    spk_game = SpkGame(spk_func, rate=rate)

    def state_func(i):
        return (ledrow.pinstate(i), ledrow.reset_dirty(i))
    led_game = LedRowGame(state_func=state_func,
                         labels=['SPK']  
                         )
    dev = CompositeGame([
                      CompositeGame(
                              [
                               led_game,
                               ],
                                align=1),
                      InfoGame(avr),
                      ])
    
    scrshot_by_exit = [(dev, image_file)] if image_file else None
    
    AvrSimMain(avr, dev, vcd, speed=speed, fps=fps, visible=visible, timeout=timeout,
               scrshot_by_exit=scrshot_by_exit).run_game()

    spk_game.terminate()
