import shutil as su
import os
import datetime as dt

import wx
import sqlitepersist as sqp

from PathZipper import PathZipper
from DocArchiver import DocArchiver

from backgroundworkers.BgBasics import *
from backgroundworkers.BgWorker import BgWorker
from PersistClasses import DataGroup, Person, PersonInfoBit, Picture, PictureInfoBit, PersonPictureInter,  Document, DocumentInfoBit, PersonDocumentInter

class BgCsvExtractorParas():
    def __init__(self, 
                 fact, 
                 targdir : str, 
                 docarchive : DocArchiver, 
                 machine_label : str,
                 changedAfter, 
                 dopersons : bool, 
                 dodocs : bool, 
                 dopics : bool):
        
        self._fact = fact
        self._dopersons = dopersons
        self._dodocs = dodocs
        self._dopics = dopics
        self._targetdir = targdir
        self._changedAfter = changedAfter
        self._docarchive = docarchive
        self._machlabel = machine_label

    def get_caftd(self):
        if self._changedAfter is None:
            return dt.datetime(1900,1,1)
        else:
            return self._changedAfter

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

    def exportclass(self, fact, excls, targpath, alteredafter, *orderby, addexp=None):
        """Export a class to a csv file and, if applicable, also export any archived files connected
            to the selected objects of that class
            fact: SQFactory to be used fpr database access
            excls: persistnet class to export
            targpath: path of folder to write all the data to
            alderedfafter: a datetime that will be used to select the data
            orderby: used for SQQuery oderBy, see there for more explanations
            addexp: an additional expression that will be applied to select the data
        """
        name = excls.get_collection_name() + ".csv"
        filepath = os.path.join(targpath, name)
        
        exp = excls.LastUpdate > alteredafter

        if addexp is not None:
            exp = (exp) & (addexp)

        q = sqp.SQQuery(fact, excls).where(exp).order_by(*orderby)
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
                                    dt.datetime(1900,1,1),
                                    DataGroup.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct
    
    def exppersons(self, fact, targpath):
        """export all person related data like seeds, groups, ..."""
        pathes = []
        sumct = 0
        
        caftd = self.paras.get_caftd()

        fpa, ct = self.exportclass(fact, 
                                   Person,
                                   targpath,
                                   caftd, 
                                   Person.Name, 
                                   Person.FirstName)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PersonInfoBit,
                                    targpath,
                                    caftd,
                                    PersonInfoBit.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct
    
    def exppics(self, fact, targpath):
        """export all person related data like seeds, groups, ..."""
        pathes = []
        sumct = 0
        caftd = self.paras.get_caftd()

        fpa, ct = self.exportclass(fact, 
                                   Picture,
                                   targpath,
                                   caftd, 
                                   Picture.Title)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PersonPictureInter,
                                    targpath,
                                    caftd,
                                    PersonPictureInter.Created)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PictureInfoBit,
                                    targpath,
                                    caftd,
                                    PictureInfoBit.Created)
        pathes.append(fpa)
        sumct += ct

        return pathes, ct
    

    def expdocs(self, fact, targpath):
        """export all document related data like documents, infobits for docs and the archived docs too"""
        pathes = []
        sumct = 0
        caftd = self.paras.get_caftd()

        fpa, ct = self.exportclass(fact, 
                                   Document,
                                   targpath,
                                   caftd, 
                                   Document.Title)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    PersonDocumentInter,
                                    targpath,
                                    caftd,
                                    PersonDocumentInter.Created)
        pathes.append(fpa)
        sumct += ct

        fpa, ct, = self.exportclass(fact,
                                    DocumentInfoBit,
                                    targpath,
                                    caftd,
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

            if not os.path.exists(targpath):
                os.makedirs(targpath)

            p = self.paras

            self.save_paras(p, targpath)
            
            if not (p._dopersons or p._dopics or p._dodocs):
                wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
                wx.PostEvent(self.notifywin, ResultEvent(1))
                return
            
            if self.abortrequested:
                wx.PostEvent(self.notifywin, ResultEvent(0, False))
                return
            
            bfnames, ct = self.expbasics(fact, targpath)
            wx.PostEvent(self.notifywin, NotifyPercentEvent(20))
            ctsum += ct

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(0, False))
                return
            
            if self.paras._dopersons:
                perfnames, ct = self.exppersons(fact, targpath)
                ctsum += ct

            wx.PostEvent(self.notifywin, NotifyPercentEvent(40))

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(0, False))
                return
            
            if self.paras._dopics:
                picfnames, ct = self.exppics(fact, targpath)
                ctsum += ct

            wx.PostEvent(self.notifywin, NotifyPercentEvent(60))  

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(0, False))
                return
            
            if self.paras._dodocs:
                docnames, ct = self.expdocs(fact, targpath)
                ctsum += ct

            wx.PostEvent(self.notifywin, NotifyPercentEvent(80))  

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(0, False))
                return
            
            self.do_zipping(targpath)
            wx.PostEvent(self.notifywin, NotifyPercentEvent(90))  

            if self.abortrequested: 
                wx.PostEvent(self.notifywin, ResultEvent(0, False))
                return
            
            su.rmtree(targpath)
        except Exception as exc:
            wx.PostEvent(self.notifywin, ResultEvent(ctsum, False))
        finally:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
            wx.PostEvent(self.notifywin, ResultEvent(ctsum))