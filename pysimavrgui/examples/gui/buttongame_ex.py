from entrypoint2 import entrypoint
from pysimavrgui.buttongame import ButtonGame
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.maingame import MainGame

@entrypoint
def start():
    def func_up1():
        print 'up1'
    def func_down1():
        print 'down1'
    def func_up2():
        print 'up2'
    def func_down2():
        print 'down2'
    dev1 = ButtonGame(hook=dict(up=func_up1, down=func_down1), label='1', shortcut='1')
    dev2 = ButtonGame(hook=dict(up=func_up2, down=func_down2), label='2', shortcut='2')

    dev=CompositeGame([dev1,dev2])
    MainGame(dev).run_game()

