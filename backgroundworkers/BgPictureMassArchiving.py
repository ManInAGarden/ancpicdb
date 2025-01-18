import os 
import datetime as dt
import shutil as shu
import sqlitepersist as sqp
import mylogger as mylo
from backgroundworkers.BgWorker import BgWorker
from backgroundworkers.BgBasics import *

from PersistClasses import Picture, DataGroup

from DocArchiver import DocArchiver

class BgPictureMassArchiving(BgWorker):
    def __init__(self, notifywin, paras : dict):
        super().__init__(notifywin)
        self.paras = paras
        self._fact = paras["fact"]
        self._files = paras["files"]
        self._logger = paras["logger"]
        self._docarchiver = paras["docarchiver"]
        self._machlabel = paras["machlabel"]

        assert type(self._files) is list
        assert type(self._logger) is mylo.Logger
        assert type(self._fact) is sqp.SQFactory
        assert type(self._docarchiver) is DocArchiver

        self._groups = None

    def run(self):
        parfact = self._fact
        logger = self._logger

        wx.PostEvent(self.notifywin, NotifyPercentEvent(0))
        lastperc = 0
        maxl = len(self._files)
        logger.info("Starting mass archiving with {} file(s)", maxl)
        #correcting self._fact here with a cloned version of the original self._fact!
        self._fact = sqp.SQFactory(parfact.Name, parfact.DbFileName) #clone the factory for this thread

        try:
            for i in range(maxl):
                fname = self._files[i]

                perc = int(100*i/maxl)

                self._do_import(fname)
                if perc - lastperc >= 10:
                    wx.PostEvent(self.notifywin, NotifyPercentEvent(perc))
                    lastperc = perc

            wx.PostEvent(self.notifywin, ResultEvent(maxl, True))
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        except Exception as exc:
            logger.error("Unexpected error during picture import on picture {}. Message: {}",
                         fname,
                         exc)
            wx.PostEvent(self.notifywin, ResultEvent(0, False))

    def _calc_title(self, filepath : str):
        """try to calculate a title from the filename
            first we split the filename at spaces and underscores to get different words, additionally we split the
            words at position where capitalization changes from non capital to capital letters
        """
        pathparts = os.path.split(filepath)
        filename = pathparts[-1]
        (name, ext) = os.path.splitext(filename)
        
        name = name.replace("\t", " ")
        name = name.replace("_", " ")
        parts = name.split() #split at any whitespace

        first = True
        answ = None
        for part in parts:
            if answ is None:
                answ = self._get_subname_parts(part)
            else:
                answ += " " + self._get_subname_parts(part)

        return answ

    def _get_subname_parts(self, txt : str):
        lastupper = True
        answ = ""
        for c in txt:
            if c.isupper(): 
                if lastupper is False:
                    answ += " "
                lastupper = True
            else:
                lastupper = False

            answ += c
        
        return answ
            
    def _calc_group(self, fpath : str) -> DataGroup:
        """Try to get a group from the parent dir where the file is located
           When we find a group with the same name - thats the group we put the
           picture data in
        """
        #cache groups
        if self._groups is None:
            self._groups = {}
            groups = sqp.SQQuery(self._fact, DataGroup).where(DataGroup.GroupType=="PICT").as_list()

            for group in groups:
                self._groups[group.name] = group

        pathdir = os.path.dirname(fpath)
        abovedirs, pardir = os.path.split(pathdir)

        if pardir in self._groups:
            return self._groups[pardir]
        else:
            return None

    def _get_best_scandate(self, fpath):
        timestamp = os.path.getctime(fpath)
        return dt.datetime.fromtimestamp(timestamp)

    def _move_file2done(self, fpath):
        logger = self._logger
        pdir,fname = os.path.split(fpath)
        targdir = os.path.join(pdir, "done")

        if not os.path.exists(targdir): os.mkdir(targdir)

        logger.debug("Moving source file <{}> to donedir <{}>",
                     fpath,
                     targdir)
        
        shu.move(fpath, targdir)
        
    def _create_readid(self):
        tsp = dt.datetime.now()
        return "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self._machlabel, tsp)

    def _do_import(self, fname):
        logger = self._logger

        logger.info("Trying to import the file <{}> to create a new picture entry in database and file archive",
                    fname)
        
        title = self._calc_title(fname)
        logger.debug("Calculated name as <{}>", title)

        grp = self._calc_group(fname)
        if grp is not None: 
            grpid = grp._id 
            logger.debug("Calculated group as <{}>", grp.name)
        else: 
            logger.debug("Did not find a group for the picture")
            grpid = None 

        archname, extname = self._docarchiver.archive_file(fname)
        logger.debug("Succesfully saved file <{}> to archive. It's now unter <>", 
                            fname,
                            archname)
        
        scandt = self._get_best_scandate(fname)
        pic = Picture(title = title, 
                        readableid = self._create_readid(),
                        groupid=grpid, 
                        filepath = archname,
                        ext = extname,
                        scandate = scandt)
        
        self._fact.flush(pic)

        self._move_file2done(fname)
        logger.info("Succesfully created new picture db entry with rid <{}> and title <{}>", 
                        pic.readableid,
                        pic.title)
