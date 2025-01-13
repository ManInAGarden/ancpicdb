from backgroundworkers.BgWorker import BgWorker
from backgroundworkers.BgBasics import *

import datetime as dt
from PathZipper import PathZipper
import os

class BgDbZipperParas():
    def __init__(self, targetdir, dbname):
        self._targetdir = targetdir
        self._dbname = dbname

class BgDbZipper(BgWorker):
    def __init__(self, notifywin, conf, logger, paras : BgDbZipperParas):
        super().__init__(notifywin)
        self._conf = conf
        self._logger = logger
        self._paras = paras

    def run(self):
        logger = self._logger
        logger.info("BgZipper startet Datenbanksicherung")

        if self.abortrequested:
             wx.PostEvent(self.notifywin, ResultEvent(0, False))
             return
        
        try:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(-1)) #show working ...

            srcpath = self._conf.get_value_interp("backup", "sourcepath")
            srcpath = os.path.join(srcpath, self._paras._dbname)
            fname = self._conf.get_value("backup", "zipname")
            dstr = "{:%Y%m%d}".format(dt.datetime.now())
            fname = fname.replace("${CreaDate}", dstr)
            fname = fname.replace("${DbName}", self._paras._dbname)

            logger.debug("Erzeuge nun einen PathZipper für das Quellverzeichnis {}, das Zielverzeichnis {} und den Dateinamen {}",
                     srcpath,
                     self._paras._targetdir,
                     fname)
        
            pz = PathZipper(srcpath, self._paras._targetdir, fname, logger)

            pz.dozip()
            logger.info("BgZipper hat Datenbanksicherung vollständig durchlaufen und endet nun")
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
            wx.PostEvent(self.notifywin, ResultEvent(1))
        except Exception as exc:
            logger.error("Unbehandelter Fehler in backupdb: {}", exc)
            wx.PostEvent(self.notifywin, NotifyPercentEvent(0))
            wx.PostEvent(self.notifywin, ResultEvent(0, False))
