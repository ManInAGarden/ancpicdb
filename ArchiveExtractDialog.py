import datetime
import GeneratedGUI as gg
import wx
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import DataGroup, Picture, Document
import backgroundworkers as bgw

class ArchiveExtractDialog(gg.gArchiveExtractDialog):
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive
    
    def __init__(self, parent, fact):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._configuration = parent.configuration
        self._docarchive = parent.docarchive
        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)


    def workerfinished(self, event):
        GuiHelper.enable_ctrls(True, self.m_startExtractionBU)
        GuiHelper.enable_ctrls(False, self.m_abortExtractionBU)

    def notifyperc(self, event):
        perc = event.data
        self.m_extractionGAUGE.SetValue(perc)

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def grp_str(self, grp : DataGroup):
        return grp.name
    
    def _filldialog(self):
        GuiHelper.enable_ctrls(False, self.m_startExtractionBU, self.m_abortExtractionBU)

        self.picture_groups = sqp.SQQuery(self._fact,DataGroup).where(DataGroup.GroupType=="PICT").order_by(DataGroup.Name).as_list()
        self.document_groups = sqp.SQQuery(self._fact,DataGroup).where(DataGroup.GroupType=="DOC").order_by(DataGroup.Name).as_list()
        
        GuiHelper.set_sqp_objval(self.m_pictureGroupCB, None, self.grp_str, self.picture_groups)
        GuiHelper.set_sqp_objval(self.m_documentGroupCB, None, self.grp_str, self.document_groups)

        maxday = datetime.datetime.now() + datetime.timedelta(days=1)
        
        GuiHelper.set_val(self.m_documentScandateDaySC, maxday.day)
        GuiHelper.set_val(self.m_pictureScandateDaySC, maxday.day)
        GuiHelper.set_val(self.m_pictureScandateMonthSC, maxday.month)
        GuiHelper.set_val(self.m_documentScandateMonthSC, maxday.month)
        GuiHelper.set_val(self.m_pictureScandateYearSC, maxday.year)
        GuiHelper.set_val(self.m_documentScandateYearSC, maxday.year)

    def picturesChecked(self, event):
        dopics = GuiHelper.get_val(self.m_doPicturesCB)
        GuiHelper.enable_ctrls(dopics,
                           self.m_pictureGroupCB,
                           self.m_pictureScandateOP,
                           self.m_pictureScandateDaySC,
                           self.m_pictureScandateMonthSC,
                           self.m_pictureScandateYearSC)

    def documentsChecked(self, event):
        dodocs = GuiHelper.get_val(self.m_doDocumentsCB)
        GuiHelper.enable_ctrls(dodocs,
                           self.m_documentGroupCB,
                           self.m_documentScandateOpCB,
                           self.m_documentScandateDaySC,
                           self.m_documentScandateMonthSC,
                           self.m_documentScandateYearSC)
        
    def startExtraction(self, event):
        targpath = GuiHelper.get_val(self.m_targetDirDIRP)
        if targpath is None or len(targpath)==0:
            return
        
        dopics = GuiHelper.get_val(self.m_doPicturesCB)
        dodocs = GuiHelper.get_val(self.m_doDocumentsCB)

        if not dopics and not dodocs:
            return
        
        GuiHelper.enable_ctrls(False, self.m_startExtractionBU)
        GuiHelper.enable_ctrls(True, self.m_abortExtractionBU)
        opl = ["=", ">", "<"]

        if dopics:
            exp = sqp.IsNotNone(Picture.Id)
            docgrp = GuiHelper.get_val(self.m_pictureGroupCB, self.picture_groups)
            if docgrp is not None:
                exp = exp & (Picture.GroupId==docgrp._id)
            scanop = GuiHelper.get_val(self.m_pictureScandateOP, opl)
            scanday = GuiHelper.get_val(self.m_pictureScandateDaySC)
            scanmonth = GuiHelper.get_val(self.m_pictureScandateMonthSC)
            scanyear = GuiHelper.get_val(self.m_pictureScandateYearSC)

            if scanyear is not None and scanmonth is not None and scanday is not None:
                expdt = datetime.datetime(scanyear, scanmonth, scanday)
                if scanop=="=":
                    exp = exp & (Picture.ScanDate == expdt)
                elif scanop == "<":
                    exp = exp & (Picture.ScanDate < expdt)
                elif scanop == ">":
                    exp = exp & (Picture.ScanDate > expdt)
                else:
                    GuiHelper.show_error("Unbekannter Operator für das Scandatum der Bilder")

            pics = sqp.SQQuery(self._fact, Picture).where(exp).as_list()
        else:
            pics = []

        if dodocs:
            exp = sqp.IsNotNone(Document.Id) #always true
            docgrp = GuiHelper.get_val(self.m_documentGroupCB, self.document_groups)
            if docgrp is not None:
                exp = exp & (Document.GroupId==docgrp._id)

            scanop = GuiHelper.get_val(self.m_documentScandateOpCB, opl)
            scanday = GuiHelper.get_val(self.m_documentScandateDaySC)
            scanmonth = GuiHelper.get_val(self.m_documentScandateMonthSC)
            scanyear = GuiHelper.get_val(self.m_documentScandateYearSC)

            if scanyear is not None and scanmonth is not None and scanday is not None:
                expdt = datetime.datetime(scanyear, scanmonth, scanday)
                if scanop=="=":
                    exp = exp & (Picture.ScanDate == expdt)
                elif scanop == "<":
                    exp = exp & (Picture.ScanDate < expdt)
                elif scanop == ">":
                    exp = exp & (Picture.ScanDate > expdt)
                else:
                    GuiHelper.show_error("Unbekannter Operator für das Scandatum der Bilder")

            docs = sqp.SQQuery(self._fact, Document).where(exp).as_list()
        else:
            docs = []

        paras = bgw.ArchExtractorParas(pics + docs,
                                       self._docarchive)
        paras.targetpath = targpath
        self.worker = bgw.BgArchiveExtractor(self, paras)
        pt = self.worker.start()
        GuiHelper.enable_ctrls(True, self.m_abortExtractionBU)
        GuiHelper.enable_ctrls(False, self.m_startExtractionBU)
            

    def abortExtraction(self, event):
        self.worker.requestabort()

    def targetDirChanged(self, event):
        dirval = GuiHelper.get_val(self.m_targetDirDIRP)
        if dirval is not None and len(dirval)>0:
            GuiHelper.enable_ctrls(True, self.m_startExtractionBU)
        else:
            GuiHelper.enable_ctrls(False, self.m_startExtractionBU)
