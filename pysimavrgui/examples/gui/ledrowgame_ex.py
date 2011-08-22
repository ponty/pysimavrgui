from entrypoint2 import entrypoint
from pysimavrgui.ledrowgame import LedRowGame
from pysimavrgui.maingame import MainGame

@entrypoint
def start():
    def func(i):
        return (i>1,i>2)
    dev = LedRowGame(func,disp_size=4,labels=['x','y','z'])
    MainGame(dev).run_game()

