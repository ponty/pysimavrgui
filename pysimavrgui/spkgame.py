import logging
import threading

try:
    import pyaudio
except ImportError:
    logging.debug('pyaudio is missing, sound is not supported')
    
chunk = 1024

class SpkGame():
    ''' sound is very poor'''
    def __init__(self, func, rate=11025):
        ''
        self.func = func
        self.rate = rate
        self._stop_thread = False
        self._thread = None
        if pyaudio:
            self.start()
            
    def start(self):
        self.p = pyaudio.PyAudio()

        # open stream
        self.stream = self.p.open(format=self.p.get_format_from_width(1),
                        channels=1,
                        rate=self.rate,
                        output=True)

        def target():
            while not self._stop_thread:
                # play stream
                data = self.func(chunk)
                if len(data):
                    self.stream.write(data)

        self._thread = threading.Thread(target=target)
        self._thread.start()


    def terminate(self):
        if pyaudio:
            self._stop_thread = True
            self._thread.join()
            self.stream.close()
            self.p.terminate()
        
