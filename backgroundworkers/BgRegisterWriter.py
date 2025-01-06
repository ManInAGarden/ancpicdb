import wx
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER

import sqlitepersist as sqp

from backgroundworkers.BgBasics import *
from backgroundworkers.BgWorker import BgWorker

from PersistClasses import _InfoBit, DataGroup, Person, PersonInfoBit, Picture, PictureInfoBit, Document, DocumentInfoBit


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
        self.styles.add(ParagraphStyle("BodyIndent", self.styles["BodyText"], leftIndent=20, KeepTogether=True))

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
        answ = "<b>" + d.readableid + "</b> "

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
        answ = "<b>" + p.readableid + "</b> "

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

    def _getsourcetxt(self, infobit : _InfoBit):
        if infobit.suppliedby is None or len(infobit.suppliedby)==0:
            return "-anonym-"
        else:
            return infobit.suppliedby
        
    def _getinfotxt(self, infobit : _InfoBit):
        if infobit.infocontent is None or len(infobit.infocontent)==0:
            return "-leer-"
        else:
            return infobit.infocontent
        
    def _getinfodatetxt(self, ib : _InfoBit):
        if ib.infodate is None:
            return "kein Datum"
        else:
            return "{:%d.%m.%Y}".format(ib.infodate)
        
    def _add_infobit(self, story, style, ib : _InfoBit):
        txt = "<b>" + self._getinfodatetxt(ib)
        txt += ", " + self._getsourcetxt(ib) + "</b>"
        txt += ": <i>" + self._getinfotxt(ib) + "</i>"
        txt = txt.replace("\n", " - ") #remove line breaks
        mystyle = self.styles["BodyIndent"]
        self._addparagraph(story, mystyle, txt)

    

    def run(self):
        #first we need to clone the factory because SQL-conn has to be created
        #in the very same thread we are using it.

        wx.PostEvent(self.notifywin, NotifyPercentEvent(-1)) #notify about activity by starting pulsing with -1

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
                fact.fill_joins(elem, Document.DocInfoBits)
                elemibits = elem.docinfobits
            elif self._docls is Picture:
                fact.fill_joins(elem, Picture.PictInfoBits)
                elemtxt = self._get_picinfo(elem)
                elemibits = elem.pictinfobits
            else:
                raise Exception("Unknown element class in run()")
                        
            self._addparagraph(story, bstyle, elemtxt)
            for elembit in elemibits:
                self._add_infobit(story, bstyle, elembit)




        self._doc.build(story)

        wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
        wx.PostEvent(self.notifywin, ResultEvent(1))