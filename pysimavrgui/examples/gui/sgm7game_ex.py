from entrypoint2 import entrypoint
from pysimavrgui.maingame import MainGame
from pysimavrgui.sgm7game import Sgm7Game


@entrypoint
def start():
    def func(x):
        return [
                (255,0),
                (0,0),
                (255,33),
                (7,0),
                ][x]
    dev = Sgm7Game(func,4)
    MainGame(dev).run_game()

