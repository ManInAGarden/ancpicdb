import GeneratedGUI as gg
import wx
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import DataGroup, GroupTypeCat

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
