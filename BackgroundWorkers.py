from threading import Thread
import time
import datetime as dt
from pathlib import Path
import wx
from DocArchiver import DocArchiver
from PathZipper import PathZipper
import sqlitepersist as sqp
import shutil as su
import os
from ABDBTools import APDBTools

from PersistClasses import DataGroup, Person, PersonInfoBit, Picture, PictureInfoBit, PersonPictureInter,  Document, DocumentInfoBit, PersonDocumentInter

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
    
    def requestabort(self):
        """request thread to be aborted when possible"""
        self.abortreq = True

    @property
    def abortrequested(self):
        """check wether abort has been requested"""
        return self.abortreq == True

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

            if self.abortrequested:
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return

        wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        wx.PostEvent(self.notifywin, ResultEvent(ct))

class BgCsvExtractorParas():
    def __init__(self, fact, targdir : str, docarchive : DocArchiver, changedAfter, dopersons, dodocs, dopics, doonlyown):
        self._fact = fact
        self._dopersons = dopersons
        self._dodocs = dodocs
        self._dopics = dopics
        self._doonlyown = doonlyown
        self._targetdir = targdir
        self._changedAfter = changedAfter
        self._docarchive = docarchive

class BgCsvExtractor(BgWorker):
    def __init__(self, notifywin, paras : BgCsvExtractorParas):
        super().__init__(notifywin)
        self.paras = paras

    def makesure_direxists(self, fname):
        """make sure the dir for a given filefame already exisist"""
        dirname = os.path.dirname(fname)
        if os.path.exists(dirname): return

        os.makedirs(dirname)


    def copyarchfile(self, archtarg, src):
        """copy an archive file (src) to the given targetdir"""
        targfname = os.path.join(archtarg, src)
        fullsrc = self.paras._docarchive.get_fullpath(src)
        self.makesure_direxists(targfname)
        su.copy2(fullsrc, targfname)

    def exportclass(self, fact, excls, targpath, alteredafter, *orderby):
        name = excls.get_collection_name() + ".csv"
        filepath = os.path.join(targpath, name)
        q = sqp.SQQuery(fact, excls).order_by(*orderby)
        with open(filepath, "w") as f:
            exp = sqp.SQLitePersistCsvExporter(excls, f)
            ct = exp.do_export(q)

        archtarg = os.path.join(targpath, "Archive")        
        if excls is Document:
            for doc in q:
                if doc.filepath is not None:
                    self.copyarchfile(archtarg, doc.filepath)

        elif excls is Picture:
            for pic in q:
                if pic.filepath is not None:
                    self.copyarchfile(archtarg, pic.filepath)

        return filepath, ct

    def expbasics(self, fact, targpath):
        """export all basic data like seeds, groups, ..."""
        pathes = []
        sumct = 0

        fpa, ct = self.exportclass(fact, 
                                   sqp.PCatalog,
                                   targpath,
                                   dt.datetime(1900,1,1), 
                                   sqp.PCatalog.Type, 
                                   sqp.PCatalog.Code)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    DataGroup,
                                    targpath,
                                    dt.datetime(1900,1,1,),
                                    DataGroup.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct
    
    def exppersons(self, fact, targpath):
        """export all person related data like seeds, groups, ..."""
        pathes = []
        sumct = 0

        fpa, ct = self.exportclass(fact, 
                                   Person,
                                   targpath,
                                   dt.datetime(1900,1,1), 
                                   Person.Name, 
                                   Person.FirstName)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PersonInfoBit,
                                    targpath,
                                    dt.datetime(1900,1,1,),
                                    PersonInfoBit.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct
    
    def exppics(self, fact, targpath):
        """export all person related data like seeds, groups, ..."""
        pathes = []
        sumct = 0

        fpa, ct = self.exportclass(fact, 
                                   Picture,
                                   targpath,
                                   dt.datetime(1900,1,1), 
                                   Picture.Title)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PersonPictureInter,
                                    targpath,
                                    dt.datetime(1900,1,1,),
                                    PersonPictureInter.Created)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PictureInfoBit,
                                    targpath,
                                    dt.datetime(1900,1,1,),
                                    PictureInfoBit.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct
    

    def expdocs(self, fact, targpath):
        """export all document related data like seeds, groups, ..."""
        pathes = []
        sumct = 0

        fpa, ct = self.exportclass(fact, 
                                   Document,
                                   targpath,
                                   dt.datetime(1900,1,1), 
                                   Document.Title)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PersonDocumentInter,
                                    targpath,
                                    dt.datetime(1900,1,1,),
                                    PersonDocumentInter.Created)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    DocumentInfoBit,
                                    targpath,
                                    dt.datetime(1900,1,1,),
                                    DocumentInfoBit.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct

    def save_paras(self, p, targp):
        parafile = os.path.join(targp, "_expparameters.txt")
        with open(parafile, "w") as f:
            f.write("Datenbankdatei: {}\n".format(p._fact.DbFileName))
            f.write("Personenexport: {}\n".format(p._dopersons))
            f.write("Dokumentenexport: {}\n".format(p._dodocs))
            f.write("Bilderexport: {}\n".format(p._dopics))
            f.write("Nur eigene Daten: {}\n".format(p._doonlyown))
            f.write("Geändert nach: {}\n".format(p._changedAfter))

    def do_zipping(self, pathtozip : str):
        head,tail = os.path.split(pathtozip)
        if head is None:
            return
        
        if not os.path.isdir(head):
            return
        
        today = dt.datetime.now()
        fname = "AncPicDbTeilexport{:%Y%m%d}.zip".format(today)
        pz = PathZipper(pathtozip, head, fname)
        pz.dozip()

        
    def run(self):
        # The factory needs to be cloned because the original was created in the
        # parent thread

        parfact = self.paras._fact
        fact = sqp.SQFactory(parfact.Name, parfact.DbFileName)

        try:
            ctsum = 0
            outer_targpath = self.paras._targetdir
            targpath = os.path.join(outer_targpath, "data")
            os.makedirs(targpath)
            p = self.paras

            self.save_paras(p, targpath)
            
            if not (p._dopersons or p._dopics or p._dodocs):
                wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
                wx.PostEvent(self.notifywin, ResultEvent(1))
                return
            
            if self.abortrequested:
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return
            
            bfnames, ct = self.expbasics(fact, targpath)
            wx.PostEvent(self.notifywin, NotifyPercentEvent(20))
            ctsum += ct

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return
            
            if self.paras._dopersons:
                perfnames, ct = self.exppersons(fact, targpath)
                ctsum += ct

            wx.PostEvent(self.notifywin, NotifyPercentEvent(40))

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return
            
            if self.paras._dopics:
                picfnames, ct = self.exppics(fact, targpath)
                ctsum += ct

            wx.PostEvent(self.notifywin, NotifyPercentEvent(60))  

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return
            
            if self.paras._dodocs:
                docnames, ct = self.expdocs(fact, targpath)
                ctsum += ct

            wx.PostEvent(self.notifywin, NotifyPercentEvent(80))  

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return
            
            self.do_zipping(targpath)
            wx.PostEvent(self.notifywin, NotifyPercentEvent(90))  

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(None))
                return
            
            su.rmtree(targpath)

        finally:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
            wx.PostEvent(self.notifywin, ResultEvent(ctsum))


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


        



        
