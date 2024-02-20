import GeneratedGUI as gg
import wx
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import DataGroup, Picture, Document
import BackgroundWorkers as bgw

class ArchiveExtractDialog(gg.gArchiveExtractDialog):
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive
    
    def __init__(self, parent, fact):
        super().__init__(parent)
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
        self.picture_groups = sqp.SQQuery(self._fact,DataGroup).where(DataGroup.GroupType=="PICT").order_by(DataGroup.Name).as_list()
        self.document_groups = sqp.SQQuery(self._fact,DataGroup).where(DataGroup.GroupType=="DOC").order_by(DataGroup.Name).as_list()
        
        GuiHelper.set_sqp_objval(self.m_pictureGroupCB, None, self.grp_str, self.picture_groups)
        GuiHelper.set_sqp_objval(self.m_documentGroupCB, None, self.grp_str, self.document_groups)

    def picturesChecked(self, event):
        dopics = GuiHelper.get_val(self.m_doPicturesCB)
        GuiHelper.enable_ctrls(dopics,
                           self.m_pictureGroupCB,
                           self.m_pictureScandateOP,
                           self.m_pictureScandateDayTB,
                           self.m_pictureScandateMonthTB,
                           self.m_pictureScandateYearTB)

    def documentsChecked(self, event):
        dodocs = GuiHelper.get_val(self.m_doDocumentsCB)
        GuiHelper.enable_ctrls(dodocs,
                           self.m_documentGroupCB,
                           self.m_documentScandateOpCB,
                           self.m_documentScandateDayTB,
                           self.m_documentScandateMonthTB,
                           self.m_documentScandateYearTB)
        
    def startExtraction(self, event):
        targpath = GuiHelper.get_val(self.m_targetDirDIRP)
        if targpath is None or len(targpath)==0:
            return
        
        dopics = GuiHelper.get_val(self.m_doPicturesCB)
        dodocs = GuiHelper.get_val(self.m_doDocumentsCB)

        GuiHelper.enable_ctrls(False, self.m_startExtractionBU)
        GuiHelper.enable_ctrls(True, self.m_abortExtractionBU)
        if dopics:
            pics = sqp.SQQuery(self._fact, Picture).as_list()
            picparas = bgw.ArchExtractorParas(pics,
                                              self._docarchive)
            picparas.targetpath = targpath
            picworker = bgw.BgArchivePicExtractor(self, picparas)
            pt = picworker.start()
            pass
        


    def abortExtraction(self, event):
        return super().abortExtraction(event)
