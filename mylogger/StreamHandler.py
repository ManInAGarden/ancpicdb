import sys
from .BasicHandler import *

class StreamHandler(BasicHandler):
    def __init__(self, stream = sys.stderr):
        super().__init__()
        self._stream = stream

    def write(self, message):
        self._stream.write(message + self._lb)

