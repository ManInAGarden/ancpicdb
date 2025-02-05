import os 
import datetime as dt
import time
import shutil as shu
import sqlitepersist as sqp
import mylogger as mylo
from backgroundworkers.BgMassArchivingBase import BgMassArchivingBase
from backgroundworkers.BgBasics import *

from PersistClasses import Picture, DataGroup

from DocArchiver import DocArchiver

class BgPictureMassArchiving(BgMassArchivingBase):
    
    def __init__(self, notifywin, paras : dict):
        super().__init__(notifywin, paras)
        self._logger.debug("Initialising BgPictureMassArchiving")

    def run(self):
        parfact = self._fact
        logger = self._logger

        wx.PostEvent(self.notifywin, NotifyPercentEvent(0))
        lastperc = 0
        maxl = len(self._files)
        logger.info("Starting picture mass archiving with {} file(s)", maxl)
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

    
            
    def _calc_group(self, fpath : str) -> DataGroup:
        """Try to get a group from the parent dir where the file is located
           When we find a group with the same name - thats the group we put the
           picture data in
        """
        return super()._calc_group(fpath, "PICT")


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
