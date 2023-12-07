import wx
import wx.adv
from PersistClasses import _InfoBit
import GeneratedGUI as gg
from GuiHelper import GuiHelper
import sqlitepersist as sqp

class EditInfoBitDialog(gg.gEditInfoBitDialog):
    def __init__(self, parent, fact : sqp.SQFactory, ib : _InfoBit):
        super().__init__(parent)
        self._fact = fact
        self._configuration = parent.configuration
        self._infobit = ib

    @property
    def infobit(self):
        return self._infobit

    def _filldialog(self):
        ib = self._infobit
        GuiHelper.set_val(self.m_infoDatumDP, ib.infodate)
        GuiHelper.set_val(self.m_infoquelleTB, ib.suppliedby)
        GuiHelper.set_val(self.m_infoTextTB, ib.infocontent)


    def showmodal(self):
        self._filldialog()

        res = self.ShowModal()

        if res == wx.ID_CANCEL:
            return res
        
        ib = self._infobit
        ib.infodate = GuiHelper.get_val(self.m_infoDatumDP)
        ib.suppliedby = GuiHelper.get_val(self.m_infoquelleTB)
        ib.infocontent = GuiHelper.get_val(self.m_infoTextTB)
        self._fact.flush(ib)
        return res