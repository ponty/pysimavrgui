from entrypoint2 import entrypoint
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.ledgame import LedGame
from pysimavrgui.maingame import MainGame

@entrypoint
def start():
    def func_on():
        return (1,0)
    def func_off():
        return (0,0)
    def func_pulse():
        return (1,1)
    dev1 = LedGame(func_on,'on')
    dev2 = LedGame(func_off,'off')
    dev3 = LedGame(func_pulse,'pulse')
    dev=CompositeGame([dev1,dev2,dev3])
    MainGame(dev).run_game()

