from .BasicHandler import *
import queue
import os
import shutil
import datetime as dt
import threading

class RotatingFileHandler(BasicHandler):
    def __init__(self, filename : str, size=5000000):
        super().__init__()

        self._size = size
        self._filename = filename
        self._lock = threading.Lock()
        self._buffer = queue.SimpleQueue()

    def _check_rotation(self):
        if os.path.exists(self._filename) and os.path.getsize(self._filename) > self._size:
            nowstr = dt.datetime.now().strftime("%Y%m%d%H%M%S")
            newname = nowstr + "_" + self._filename
            shutil.move(self._filename, newname)

    def write(self, msg : str):
        try:
            self._lock.acquire()
            self._check_rotation()
            try:
                with open(self._filename, "a") as f:
                    while not self._buffer.empty():
                        qmsg = self._buffer.get()
                        f.write(qmsg + "QUEUED" + self._lb)
                
                    f.write(msg + self._lb)
            except Exception as exc:
                self._buffer.put(msg)
        finally:
            self._lock.release()
