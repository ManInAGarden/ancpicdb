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
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER

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
        try:
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
        finally:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
            wx.PostEvent(self.notifywin, ResultEvent(ct))

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
        """export all document related data like seeds, groups, ..."""
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


class BgRegisterWriter(BgWorker):
    def __init__(self, notifywin, paras : dict):
        super().__init__(notifywin)
        self.paras = paras
        self._fact = paras["fact"]
        self._docls = paras["docls"]
        self.targetfile = paras["targetfile"]
        self.title = paras["title"]

        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle("Heading1tog", self.styles["Heading1"], keepWithNext=True))
        self.styles.add(ParagraphStyle("Heading2tog", self.styles["Heading2"], keepWithNext=True))
        self.styles.add(ParagraphStyle("Heading3tog", self.styles["Heading3"], keepWithNext=True))

        self._doc = SimpleDocTemplate(self.targetfile, pagesize = A4)

    def _addparagraph(self, story, style, txt : str = None):
        if txt is None:
            return
        
        txt = txt.replace('\n','<br />')
        txt = txt.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;')

        pg = Paragraph(txt, style)

        story.append(pg)


    def _get_docinfo(self, doc) -> str:
        if doc is None:
            return "?"
        
        d = doc
        answ = d.readableid + " "

        if d.documentgroup is not None: answ += ", Gruppe: <i>" + d.documentgroup.name + "</i>"
        if d.type is not None: answ += ", Dokumentart: <i>" + d.type.value + "</i>"

        answ += ", Titel: <i>" + d.title + "</i>"

        if d.productiondate is not None: 
            answ += ", erstellt am: <i>" + "{}.{}.{}".format(d.productiondate.day, d.productiondate.month, d.productiondate.year) + "</i>"
        if d.scandate is not None: 
            answ += ", gescannt am: <i>" + "{}.{}.{}".format(d.scandate.day, d.scandate.month, d.scandate.year) + "</i>"

        return answ
    
    def _get_picinfo(self, pic) -> str:
        if pic is None:
            return "?"

        p = pic
        answ = p.readableid + " "

        if p.picturegroup is not None:
            answ += ", Gruppe: <i>" + p.picturegroup.name + "</i>"

        answ += ", Titel: <i>" + p.title + "</i>"
        takendate = p.best_takendate
        if takendate[2] is not None: #we have at least a year
            taks = takendate[2].__str__()
            if takendate[1] is not None:
                taks = takendate[1].__str__() + "." + taks
                if takendate[0] is not None:
                    taks = takendate[0].__str__() + "." + taks

            answ += ", aufgenommen: <i>" + taks + "</i>"

        if p.scandate is not None:
            answ += ", gescannt am: <i>" + "{}.{}.{}".format(p.scandate.day, p.scandate.month, p.scandate.year) + "</i>"

        return answ

    def run(self):
        #first we need to clone the factory because SQL-conn has to be created
        #in the very same thread we are using it.

        parfact = self._fact
        fact = sqp.SQFactory(parfact.Name, parfact.DbFileName)

        q = sqp.SQQuery(fact, self._docls).order_by(self._docls.ReadableId)

        story = [Spacer(1, 2.0*cm)]
        bstyle = self.styles["BodyText"]
        head2s = self.styles["Heading2tog"]
        itstyle = self.styles["Italic"]
        
        self._addparagraph(story, head2s, self.title)
        
        for elem in q:
            if self._docls is Document:
                elemtxt = self._get_docinfo(elem)
            elif self._docls is Picture:
                elemtxt = self._get_picinfo(elem)
            else:
                raise Exception("Unknown element class in run()")
            
            self._addparagraph(story, bstyle, elemtxt)


        self._doc.build(story)

        wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        wx.PostEvent(self.notifywin, ResultEvent(1))


        



        
