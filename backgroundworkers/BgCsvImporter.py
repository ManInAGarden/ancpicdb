import tempfile as tf
import zipfile as zf
import os
import shutil
import wx
import sqlitepersist as sqp
import mylogger as mylo
from DocArchiver import DocArchiver


from backgroundworkers.BgBasics import *
from backgroundworkers.BgWorker import BgWorker
from PersistClasses import DataGroup, Person, PersonInfoBit, Picture, PictureInfoBit, PersonPictureInter,  Document, DocumentInfoBit, PersonDocumentInter


class BgCsvImporterParas():
    def __init__(self, 
                 fact, 
                 zipfile : str, 
                 docarchive : DocArchiver,
                 logger : mylo.Logger):
        
        self._fact = fact
        self._zipfile = zipfile
        self._logger = logger
        self._docarchive = docarchive

class BgCsvImporter(BgWorker):
    def __init__(self, notifywin, paras : BgCsvImporterParas):
        super().__init__(notifywin)
        self.paras = paras

    def _extract_zip(self, zipfilename, ziptod : tf.TemporaryDirectory):
        logger = self.paras._logger
        
        zipf = zf.ZipFile(zipfilename)
        zippath = ziptod

        logger.debug("Extracting the zipfile {} to a temporary path named {} now",
                     zipfilename,
                     zippath)
        
        zipf.extractall(zippath)


    def _import_class(self, impcls, zipd, fact : sqp.SQFactory, findwith:list=[]) -> int:
        logger = self.paras._logger
        imp = sqp.SQLitePersistCsvImporter(impcls, fact, findwith=findwith)
        fname = sqp.SQLitePersistCsvImporter.get_std_fname(impcls)
        fname = os.path.join(zipd, "data", fname)
        logger.debug("Csv importing from {} now", fname)
        ct = 0
        with open(fname, "r") as f:
            ct = imp.do_import(f)
        
        return ct

    def _import_basics(self, zipd, fact : sqp.SQFactory) -> int:
        logger = self.paras._logger
        logger.debug("Importing basic objects now")
        sumct = 0
        sumct += self._import_class(sqp.PCatalog, 
                                    zipd, 
                                    fact, 
                                    findwith=[sqp.PCatalog.Code, sqp.PCatalog.Type, sqp.PCatalog.LangCode])
        sumct += self._import_class(DataGroup, zipd, fact)
        logger.debug("Finished importing basic objects now, did {} catalog entries and data groups", sumct)
        
        return sumct


    def _import_persons(self, zipd, fact : sqp.SQFactory) -> int:
        logger = self.paras._logger
        logger.debug("Importing person data now")
        sumct = 0
        pct = self._import_class(Person, zipd, fact)
        sumct += pct
        ibct = self._import_class(PersonInfoBit, zipd, fact)
        sumct += ibct
        logger.debug("Finished importing person related data related now, imported {} persons and {} person-info-bits.",
                     pct,
                     ibct)

        return sumct


    def _import_documents(self, zipd, fact : sqp.SQFactory) -> int:
        logger = self.paras._logger
        logger.debug("Importing document related data now")
        docct = self._import_class(Document, zipd, fact)
        docict = self._import_class(DocumentInfoBit, zipd, fact)
        pdocintct = self._import_class(PersonDocumentInter, zipd, fact)

        logger.debug("Finished document import, did {} documents, {} document-info-bits and {} person-documents-intersections",
                     docct,
                     docict,
                     pdocintct)
        
        return docct + docict + pdocintct

    def _import_pictures(self, zipd, fact : sqp.SQFactory) -> int:
        logger = self.paras._logger
        logger.debug("Importing picture related data now")
        pi_ct = self._import_class(Picture, zipd, fact)
        piin_ct = self._import_class(PictureInfoBit, zipd, fact)
        per_pi_ct = self._import_class(PersonPictureInter, zipd, fact)

        logger.debug("Finished picture import, did {} pictures, {} picture-info-bits and {} person-picture-intersections.",
                     pi_ct,
                     piin_ct,
                     per_pi_ct)
        
        return  pi_ct + piin_ct + per_pi_ct
        
    def _merge_archives(self, targarchdir, srcarchdir):
        shutil.copytree(srcarchdir, targarchdir, dirs_exist_ok=True)

    def run(self):
        # The factory needs to be cloned because the original was created in the
        # parent thread

        parfact = self.paras._fact
        logger = self.paras._logger
        fact = sqp.SQFactory(parfact.Name, parfact.DbFileName) #clone the factory for this thread

        zipfile = self.paras._zipfile
        logger.info("Starting csv-import bg job for zipfile <{}>", zipfile)
        fact.begin_transaction("csv-import")
        try:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(0))
            with tf.TemporaryDirectory("ANCCSVIMP") as tdir:
                self._extract_zip(zipfile, tdir)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(10))
                bsum = self._import_basics(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(20))
                pesum = self._import_persons(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(30))
                dsum = self._import_documents(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(50))
                pisum = self._import_pictures(tdir, fact)
                wx.PostEvent(self.notifywin, NotifyPercentEvent(70))
                srcarchdir = os.path.join(tdir, "data/Archive")
                targarchdir = self.paras._docarchive._basepath
                self._merge_archives(targarchdir, srcarchdir)

            logger.info("Ended and commited csv-import bg job with {} basic objects, {} persons, {} documents and {} pictures",
                        bsum,
                        pesum,
                        dsum,
                        pisum)
            
            wx.PostEvent(self.notifywin, ResultEvent(bsum + pesum + dsum + pisum, True))
            fact.commit_transaction("csv-import")
        except Exception as exc:
            logger.error("Unexpected error, rolling back: Original message {}", str(exc))
            fact.rollback_transaction("csv-import")
            wx.PostEvent(self.notifywin, ResultEvent(0, False))
        finally:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
