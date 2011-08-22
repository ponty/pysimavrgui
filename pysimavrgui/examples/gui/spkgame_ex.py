from entrypoint2 import entrypoint
from pysimavrgui.spkgame import SpkGame
import time

@entrypoint
def start():
    data= 20*'\0'+20*'Z'
    def func(size):
        return data * (size/40)
    spk = SpkGame(func)
    time.sleep(3)
    spk.terminate()