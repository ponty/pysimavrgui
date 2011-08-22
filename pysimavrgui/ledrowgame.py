from pysimavrgui.compgame import CompositeGame
from pysimavrgui.ledgame import LedGame



class LedRowGame(CompositeGame):
    def __init__(self, state_func, disp_size=None, labels=None, align=0, size='auto'):
        if disp_size is None and labels is None:
            raise ValueError('disp_size is None and labels is None')

        if disp_size is None:
            disp_size = len(labels)
        
        self.disp_size = disp_size
        self.leds = []
        self.state_func = state_func
        for i in xrange(self.disp_size):
            s = None
            if labels:
                if i<len(labels):
                    s = labels[i]
            led = LedGame(state_func=self._get_single_state_func(i), label=s)
            self.leds += [led]

        CompositeGame.__init__(self, self.leds, align=align, size=size)
        
    def _get_single_state_func(self, i):
        def f():
            return self.state_func(i)
        return f
    
        
