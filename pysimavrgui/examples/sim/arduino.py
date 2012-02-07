'''

lcd:

#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 10, 5, 4, 3, 2);

void setup() {
  lcd.begin(16, 2);
  lcd.println("hello, world!");
}

void loop() {
}

connect UDP with netcat:
nc -u 127.0.0.1 4321

'''
from entrypoint2 import entrypoint
from path import path
from pysimavr.avr import Avr
from pysimavr.button import Button
from pysimavr.connect import connect_pins_by_rule
from pysimavr.firmware import Firmware
from pysimavr.lcd import Lcd
from pysimavr.ledrow import LedRow
from pysimavr.spk import Spk
from pysimavr.udp import Udp
from pysimavr.udpreader import UdpReader
from pysimavr.vcdfile import VcdFile
from pysimavrgui.buttongame import ButtonGame
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.examples.sim.avrsimmain import AvrSimMain
from pysimavrgui.infogame import InfoGame
from pysimavrgui.lcdgame import LcdGame
from pysimavrgui.ledrowgame import LedRowGame
from pysimavrgui.spkgame import SpkGame
from pysimavrgui.textgame import TextGame
import os
import sys
import tempfile
import time
try:
    import pyavrutils
except ImportError:
    pyavrutils = None


        

def lastline(s):
    if s:
        s = s.splitlines(1)[-1]        
    return s

def find_elf():
    build_dirs = [x for x in path(tempfile.gettempdir()).dirs('build*.tmp')]
    
    elfs = []
    
    last = path(os.getenv("HOME")) / '.arduino_last_elf'
    if not last.exists():
        last.makedirs()
    elfs += last.files()
        
    for d in build_dirs:
        elfs += [x for x in d.files('*.elf')] 
    elfs.sort(key=path.getmtime, reverse=1) 

    assert len(elfs), 'No elf file found in "%s"! Start arduino and build a sketch!' % tempfile.gettempdir()
    elf = elfs[0]
    
#    if last == elf and len(elfs) > 1:
#        if last.mtime == elfs[1].mtime:
#            elf = elfs[1]
    
    # save last elf
    if elf.parent != last:
        elf.copy(last / elf.name)
    
    return elf


           
@entrypoint
def arduino_sim(
            elf='',
            mcu='atmega168',
            f_cpu=16000000,
            vcdfile='arduino.vcd',
            speed=1,
            fps=20,
            timeout=0.0,
            visible=1,
            image_file='',
            rate=11025,
            buttons_enable=1,
            vcd_enable=0,
            spk_enable=0,
            udp_enable=1,
            avcc=5000,
            vcc=5000,
            code=None,
            ):
    '''
    
    MCU:
     - atmega168 OK 
     - atmega328p OK
     - atmega2560 NO
     - atmega1280 NO
     
    :param mcu: 
    :param avcc: AVcc  in mV
    :param vcc: Vcc  in mV
    
    '''

    if code and pyavrutils:
        cc = pyavrutils.Arduino()
        cc.build(code)
        elf = cc.output
   
    if not elf:
        elf = find_elf()
    firmware = Firmware(elf)
    avr = Avr(mcu=mcu, f_cpu=f_cpu, vcc=vcc / 1000.0, avcc=avcc / 1000.0)
    avr.load_firmware(firmware)
    
    udpReader = UdpReader()
    
    if udp_enable:
        udp = Udp(avr)
        udp.connect()
        udpReader.start()
        
    lcd = Lcd(avr)

    vcd = VcdFile(avr, period=1000, filename=vcdfile) if vcd_enable else None
    ledrow = LedRow(avr, size=14)
    buttons = [Button(avr, pullup=0) for x in range(14)] if buttons_enable else 14 * [None]
    spk = Spk(avr, rate=rate, speed=speed) if spk_enable else None
    
    
    
    connect_pins_by_rule('''
                        but0 .OUT ==> avr.D0 ==> dig.0  -> vcd
                        but1 .OUT ==> avr.D1 ==> dig.1  -> vcd
                        but2 .OUT ==> avr.D2 ==> dig.2  -> vcd
                        but3 .OUT ==> avr.D3 ==> dig.3  -> vcd
                        but4 .OUT ==> avr.D4 ==> dig.4  -> vcd
                        but5 .OUT ==> avr.D5 ==> dig.5  -> vcd
                        but6 .OUT ==> avr.D6 ==> dig.6  -> vcd
                        but7 .OUT ==> avr.D7 ==> dig.7  -> vcd

                        but8 .OUT ==> avr.B0 ==> dig.8  -> vcd
                        but9 .OUT ==> avr.B1 ==> dig.9  -> vcd
                        but10.OUT ==> avr.B2 ==> dig.10 -> vcd
                        but11.OUT ==> avr.B3 ==> dig.11 -> vcd
                        but12.OUT ==> avr.B4 ==> dig.12 -> vcd
                        but13.OUT ==> avr.B5 ==> dig.13 -> vcd

                        dig.13 --> spk.IN -> vcd
                        
                        dig.5 <=> lcd.D4 -> vcd
                        dig.4 <=> lcd.D5 -> vcd
                        dig.3 <=> lcd.D6 -> vcd
                        dig.2 <=> lcd.D7 -> vcd
                        
                        dig.12 ==> lcd.RS -> vcd
                        dig.11 ==> lcd.RW -> vcd
                        dig.10 ==> lcd.E  -> vcd
                        ''',
                         dict(
                             avr=avr,
                             dig=ledrow,
                             lcd=lcd,
                             spk=spk,
                             **dict([('but' + str(i), b) for i, b in enumerate(buttons)])
                             ),
                         vcd=vcd,
    )
    #################
    # GUI
    #################
    if spk_enable:
        def spk_func(size):
            return spk.read()
        spk_game = SpkGame(spk_func, rate=rate)

    def state_func(i):
        return (ledrow.pinstate(i), ledrow.reset_dirty(i))
    led_game = LedRowGame(state_func=state_func,
                          labels=[str(x) for x in range(14)],
                          align=1,)
        
    but_guis = [ButtonGame(
                              label=label,
                              shortcut=shortcut,
                              hook=dict(up=x.up, down=x.down) if x else {},
                              size=(50, 30),
                              ) for x, label, shortcut in zip(
                                             buttons,
                                             '0 1 2 3 4 5 6 7 8 9 10 11 12 13'.split(),
                                             '0 1 2 3 4 5 6 7 8 9 a b c d'.split(),
                                             )
                   ]
    info = InfoGame(avr)
    def reload_firmware():
        firmware = Firmware(find_elf())
        avr.load_firmware(firmware)
        lcd.reset()
        info.reload()
        
    class MyFloat(object):
        def __init__(self, value=0.0):
            self.value = value
        def __float__(self):
            return float(self.value)
        def inc(self):
            self.value *= 10.0
        def dec(self):
            self.value /= 10.0
    speed = MyFloat(speed)
    
    def udp_read():
        if not hasattr(udp_read, 'display'):
            udp_read.display = ''
        if not hasattr(udp_read, 'lastline'):
            udp_read.lastline = ''
        s = udpReader.read()
        if s:
            sys.stdout.write(s)
            udp_read.lastline += s
            udp_read.lastline = lastline(udp_read.lastline)
            udp_read.display = udp_read.lastline.replace('\n', '\\n').replace('\r', '\\r')
        return  udp_read.display
    
    dev = CompositeGame([
                        CompositeGame([led_game,
                                       CompositeGame(but_guis, align=1),
                                       ], align=0),
                        info,
                        CompositeGame([
                            CompositeGame([
                                ButtonGame(label='reload',
                                           shortcut='r',
                                           hook=dict(down=reload_firmware)),
                                ButtonGame(label='speed up',
                                           shortcut='+',
                                           hook=dict(down=speed.inc)),
                                ButtonGame(label='speed down',
                                           shortcut='-',
                                           hook=dict(down=speed.dec)),
                                TextGame((lambda : "speed set= %fx" % float(speed))),
                                           ], align=1),
                                       
                                LcdGame(lambda x, y:lcd.get_char(x, y), (16, 2)),
                                TextGame((lambda : 'ser=' + udp_read())),
                                ], align=1)
                       ])

    scrshot_by_exit = [(dev, image_file)] if image_file else None
    
    class ArduinoMain(AvrSimMain):
        bufpos = 0
        def cb_loop(self):
            AvrSimMain.cb_loop(self)
#            if len(udpReader.buffer) > self.bufpos:
#                sys.stdout.write(''.join(udpReader.buffer[self.bufpos:]))
#                self.bufpos = len(udpReader.buffer)

    sim = ArduinoMain(avr, dev, vcd, speed=speed, fps=fps, visible=visible, timeout=timeout,
               scrshot_by_exit=scrshot_by_exit)
    sim.run_game()
    
    time.sleep(1)
    if spk_enable:
        spk_game.terminate()

    if udp_enable:
        udp.terminate()
        
    if udp_enable:
        udpReader.terminate()
#        return udpReader.buffer

