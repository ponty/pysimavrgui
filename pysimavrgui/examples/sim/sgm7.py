from entrypoint2 import entrypoint
from path import path
from pysimavr.avr import Avr
from pysimavr.connect import connect_pins_by_rule
from pysimavrgui.examples.sim.avrsimmain import AvrSimMain
from pysimavr.firmware import Firmware
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.infogame import InfoGame
from pysimavrgui.ledrowgame import LedRowGame
from pysimavrgui.sgm7game import Sgm7Game
from pysimavr.inverter import Inverter
from pysimavr.ledrow import LedRow
from pysimavr.sgm7 import Sgm7
from pysimavr.vcdfile import VcdFile

@entrypoint
def run_sim(vcdfile='sgm7.vcd', speed=0.001, fps=20, timeout=0.0, visible=1, image_file=''):
    firmware = Firmware(path(__file__).dirname() / 'sgm7.elf')
    firmware.f_cpu = 8000000
    firmware.mcu = "atmega168"
    avr = Avr(firmware)
    vcd = VcdFile(avr, period=1000, filename=vcdfile)

    ####################################################
    # ledrow
    ledrow = LedRow(avr, size=12)
    
    ####################################################
    # ledrow game
    def state_func_seg(i):
        return (ledrow.pinstate(i), ledrow.reset_dirty(i))
    led_game_seg = LedRowGame(state_func=state_func_seg,
                         disp_size=8,
                         labels=['B' + str(x) for x in range(8)]  
                         )
    def state_func_dig(i):
        return (ledrow.pinstate(i + 8), ledrow.reset_dirty(i + 8))
    led_game_dig = LedRowGame(state_func=state_func_dig,
                         disp_size=4,
                         labels=['C' + str(x) for x in range(4)])
    ####################################################
    # sgm7
    sgm7 = Sgm7(avr, size=4)

    inv = [Inverter(avr) for x in range(4)]
    
    connect_pins_by_rule('''
                        ledrow.0 <== avr.B0 ==> sgm7.A -> vcd
                        ledrow.1 <== avr.B1 ==> sgm7.B -> vcd
                        ledrow.2 <== avr.B2 ==> sgm7.C -> vcd
                        ledrow.3 <== avr.B3 ==> sgm7.D -> vcd
                        ledrow.4 <== avr.B4 ==> sgm7.E -> vcd
                        ledrow.5 <== avr.B5 ==> sgm7.F -> vcd
                        ledrow.6 <== avr.B6 ==> sgm7.G -> vcd
                        ledrow.7 <== avr.B7 ==> sgm7.P -> vcd
                        
                        ledrow.8 <== avr.C0 ==> inv0.IN | inv0.OUT -> sgm7.D0 -> vcd
                        ledrow.9 <== avr.C1 ==> inv1.IN | inv1.OUT -> sgm7.D1 -> vcd
                        ledrow.10<== avr.C2 ==> inv2.IN | inv2.OUT -> sgm7.D2 -> vcd
                        ledrow.11<== avr.C3 ==> inv3.IN | inv3.OUT -> sgm7.D3 -> vcd
                        ''',
                         dict(
                             avr=avr,
                             sgm7=sgm7,
                             ledrow=ledrow,
                             inv0=inv[0],
                             inv1=inv[1],
                             inv2=inv[2],
                             inv3=inv[3],
                             ),
                         vcd=vcd,
                         )

    ####################################################
    # sgm7 game
    def segments_func(digit_index):
        return (sgm7.digit_segments(digit_index), sgm7.reset_dirty(digit_index))
    sgm7_game = Sgm7Game(segments_func=segments_func, disp_size=4)
         
    ####################################################
    # compose game
    dev = CompositeGame([
                      CompositeGame(
                              [
                               sgm7_game,
                               led_game_seg,
                               led_game_dig,
                               ],
                                    align=1),
                      InfoGame(avr),
                      ])
    
    scrshot_by_exit = [(dev, image_file)] if image_file else None
    
    AvrSimMain(avr, dev, vcd, speed=speed, fps=fps, visible=visible, timeout=timeout,
               scrshot_by_exit=scrshot_by_exit).run_game()

