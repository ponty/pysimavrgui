from entrypoint2 import entrypoint
from pysimavrgui.compgame import CompositeGame
from pysimavrgui.maingame import MainGame
from pysimavrgui.textgame import TextGame

@entrypoint
def start():
    def func1():
        return 'hello'
    def func2():
        return 'hi'
    dev1 = TextGame(func1)
    dev2 = TextGame(func2)
    dev=CompositeGame([dev1,dev2],align=1)
    MainGame(dev).run_game()

