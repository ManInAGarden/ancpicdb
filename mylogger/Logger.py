from enum import Enum
import datetime as dt
from .BasicHandler import *

class LogLevelEnum(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40

    @classmethod
    def getfromstr(cls, val : str):
        if val==cls.DEBUG.name:
            return LogLevelEnum.DEBUG
        elif val == cls.INFO.name:
            return LogLevelEnum.INFO
        elif val == cls.WARNING.name:
            return LogLevelEnum.WARNING
        elif val == cls.ERROR.name:
            return LogLevelEnum.ERROR
        else:
            raise Exception("Unknow log level <{}> cannot be transformed from str to enum".format(val))

class Logger():

    def __init__(self, level : str | LogLevelEnum, frm : str="{asctime} {level}: {message}"):
        lt = type(level)
        if lt is str:
            thislevel = LogLevelEnum.getfromstr(level)
        elif lt is LogLevelEnum :
            thislevel = level
        else:
            raise Exception("Unknow message level {} in Logger instantation".format(str(lt)))
                            
        self._level = thislevel
        self._basicfrm = frm
        self._timeformat = "%d.%m.%Y %H:%M:%S,%f"
        self._handlers = []

    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, val : LogLevelEnum):
        self._level = val

    def debug(self, frm : str, *args):
        self._log(LogLevelEnum.DEBUG, frm, *args)

    def info(self, frm : str, *args):
        self._log(LogLevelEnum.INFO, frm, *args)

    def warning(self, frm : str, *args):
        self._log(LogLevelEnum.WARNING, frm, *args)

    def error(self, frm : str, *args):
        self._log(LogLevelEnum.ERROR, frm, *args)

    def add_handler(self, handler : BasicHandler):
        hand = handler
        self._handlers.append(hand)
        return hand

    def _log(self, level : LogLevelEnum, frm : str, *args):
        if level.value < self._level.value: return

        if self._handlers is None or len(self._handlers)==0:
            raise Exception("No handlers have been defined for this logger")
        
        message = self._create_msg(frm.format(*args), level)

        for handler in self._handlers:
            if handler.isactive:
                handler.write(message)

    def _create_msg(self, msg : str, level : LogLevelEnum) -> str:
        if self._basicfrm is None:
            raise Exception("No message format in _create_msg!")
        
        answ = self._basicfrm.replace("{message}", msg)
        answ = answ.replace("{asctime}", dt.datetime.now().strftime(self._timeformat))
        answ = answ.replace("{level}", level.name)
        
        return answ