import os
import shutil as su
import wx
from backgroundworkers.BgWorker import BgWorker
from backgroundworkers.BgBasics import *

from ABDBTools import APDBTools

class DbCreatorParas():
    def __init__(self, storagepath, new_db_name, copy_old=False, old_db_name=None):
        self.new_db_name = new_db_name
        self.copy_old = copy_old
        self.storage_path = storagepath
        self.old_db_name = old_db_name

class BgDBCreator(BgWorker):
    def __init__(self, notifywin, conf, logger, paras : DbCreatorParas):
        super().__init__(notifywin)
        self.paras = paras
        self._configuration = conf
        self.logger = logger

    def run(self):
        storage_path = self.paras.storage_path
        new_db_name = self.paras.new_db_name
        old_db_name = self.paras.old_db_name
        do_copy = self.paras.copy_old

        newdirname = os.path.join(storage_path, new_db_name)
        wx.PostEvent(self.notifywin, NotifyPercentEvent(-1)) #let the activity gauge pulse to show activity
        
        if do_copy:
            self.logger.info("Kopiere DB %s nach %s", old_db_name, new_db_name)
            olddirname = os.path.join(storage_path, old_db_name)
            su.copytree(olddirname, newdirname)
            self.logger.info("Die Datenbank wurde nach %s kopiert", newdirname)
        else:
            dbfilename = self._configuration.get_value_interp("database", "filename")
            dbfilename = os.path.basename(dbfilename)
            newdirname = os.path.join(storage_path, new_db_name)
            newdbfilename = os.path.join(newdirname, dbfilename)
            self.logger.info("Erzeuge eine neue Datenbank im Verzeichnis %s", newdirname)
            dbt = APDBTools(self._configuration, self.logger)
            newdbfact = dbt.init_db("AncPicDb", newdbfilename)
            wx.PostEvent(self.notifywin, NotifyPercentEvent(50))
            newarchdir = os.path.join(newdirname, "Archive")
            newarchive = dbt.init_archive(newarchdir)
            
        wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        wx.PostEvent(self.notifywin, ResultEvent(1))