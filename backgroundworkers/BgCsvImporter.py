import tempfile as tf
import zipfile as zf
import wx
import sqlitepersist as sqp

from DocArchiver import DocArchiver


from backgroundworkers.BgBasics import *
from backgroundworkers.BgWorker import BgWorker
from PersistClasses import DataGroup, Person, PersonInfoBit, Picture, PictureInfoBit, PersonPictureInter,  Document, DocumentInfoBit, PersonDocumentInter


class BgCsvImporterParas():
    def __init__(self, 
                 fact, 
                 zipfile : str, 
                 docarchive : DocArchiver):
        
        self._fact = fact
        self._zipfile = zipfile
        self._docarchive = docarchive

class BgCsvImporter(BgWorker):
    def __init__(self, notifywin, paras : BgCsvImporterParas):
        super().__init__(notifywin)
        self.paras = paras

    def _extract_zip(self, zipfilename, ziptod : tf.TemporaryDirectory):
        zipf = zf.ZipFile(zipfilename)
        zippath = ziptod
        zipf.extractall(zippath)


    def _import_class(self, impcls, zipd, fact : sqp.SQFactory) -> int:
        imp = sqp.SQLitePersistCsvImporter(impcls, fact)
        fname = sqp.SQLitePersistCsvImporter.get_std_fname(impcls)
        with open(fname, "r") as f:
            ct += imp.do_import(f)
        
        return ct

    def _import_basics(self, zipd, fact : sqp.SQFactory) -> int:
        sumct = 0
        sumct += self._import_class(sqp.PCatalog, zipd, fact)
        sumct += self._import_class(DataGroup, zipd, fact)
        
        return sumct


    def _import_persons(self, zipd, fact : sqp.SQFactory) -> int:
        sumct = 0
        sumct += self._import_class(Person, zipd, fact)
        sumct += self._import_class(PersonInfoBit, zipd, fact)

        return sumct


    def _import_documents(self, zipd, fact : sqp.SQFactory) -> int:
        sumct = 0
        sumct += self._import_class(Document, zipd, fact)
        sumct += self._import_class(DocumentInfoBit, zipd, fact)
        sumct += self._import_class(PersonDocumentInter, zipd, fact)

        return sumct

    def _import_pictures(self, zipd, fact : sqp.SQFactory) -> int:
        sumct = 0
        sumct += self._import_class(Picture, zipd, fact)
        sumct += self._import_class(PictureInfoBit, zipd, fact)
        sumct += self._import_class(PersonPictureInter, zipd, fact)

        return sumct
        

    def run(self):
        # The factory needs to be cloned because the original was created in the
        # parent thread

        parfact = self.paras._fact
        fact = sqp.SQFactory(parfact.Name, parfact.DbFileName) #clone the factory for this thread

        zipfile = self.paras._zipfile
        fact.begin_transaction("starting csv-import transaction")
        try:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(0))
            with tf.TemporaryDirectory("ANCCSVIMP") as tdir:
                self._extract_zip(zipfile, tdir)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(10))
                self._import_basics(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(20))
                self._import_persons(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(40))
                self._import_documents(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(70))
                self._import_pictures(tdir, fact)
            fact.commit_transaction("commiting csv-import transaction")
        except Exception as exc:
            fact.rollback_transaction("error during csv-import - rolling back")
        finally:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
            wx.PostEvent(self.notifywin, ResultEvent(1))
