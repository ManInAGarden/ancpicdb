from threading import Thread
import time
from pathlib import Path
import wx
import sqlitepersist as sqp
import shutil as su
import os
from DataBaseTools import DataBaseTools

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
EVT_NOTIFYPERC_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

def EVT_NOTIFY_PERC(win, func):
    """Define Notification Event."""
    win.Connect(-1, -1, EVT_NOTIFYPERC_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
      """Init Result Event."""
      wx.PyEvent.__init__(self)
      self.SetEventType(EVT_RESULT_ID)
      self.data = data

class NotifyPercentEvent(wx.PyEvent):
    def __init__(self, perc):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NOTIFYPERC_ID)
        self.data = perc

class BgWorker(Thread):
    def __init__(self, notifywin):
        super().__init__()
        self.notifywin = notifywin
        self.abortreq = False

    def run(self):
        raise Exception("Override method 'run' in your derived background worker class!")
    
    def abort(self):
        self.abortreq = True

class ArchExtractorParas():
    def __init__(self, objects_lst, docarchive):
        self.objects = objects_lst
        self.docarchive = docarchive
        self.targetpath = None
        self.group = None
        self.scandateOp = None
        self.scandateday = None
        self.scandatemonth = None
        self.scandateyear = None

class BgArchiveExtractor(BgWorker):
    def __init__(self, notifywin, paras : ArchExtractorParas):
        super().__init__(notifywin)
        self.paras = paras

    def run(self):
        objs = self.paras.objects
        da = self.paras.docarchive
        max = len(objs)
        ct = 0
        oldperc = 0
        for obj in objs:
            ct += 1
            extname = da.extract_file(obj.filepath, self.paras.targetpath)
            extpath = Path(extname)
            targname = Path(extpath.parent, obj.readableid + extpath.suffix)
            extpath.rename(targname)
            perc = int(ct/max * 100)
            if perc != oldperc:
                wx.PostEvent(self.notifywin, NotifyPercentEvent(perc))
                oldperc = perc

            if self.abortreq:
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return

        wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        wx.PostEvent(self.notifywin, ResultEvent(ct))


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
        
        if do_copy:
            olddirname = os.path.join(storage_path, old_db_name)
            su.copytree(olddirname, newdirname)
        else:
            dbfilename = self._configuration.get_value_interp("database", "filename")
            dbfilename = os.path.basename(dbfilename)
            newdirname = os.path.join(storage_path, new_db_name)
            newdbfilename = os.path.join(newdirname, dbfilename)
            dbt = DataBaseTools(self._configuration, self.logger, "AncPicDb", newdbfilename)
            newdbfact = dbt.init_db()
            
        wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        wx.PostEvent(self.notifywin, ResultEvent(1))


        



        
