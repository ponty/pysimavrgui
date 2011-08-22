from entrypoint2 import entrypoint
from pysimavrgui.lcdgame import LcdGame
from pysimavrgui.maingame import MainGame

@entrypoint
def start():
    def char_func(x,y):
        return chr(ord('a')+x+y)
    lcd = LcdGame(char_func,(11,4))
    MainGame(lcd).run_game()
