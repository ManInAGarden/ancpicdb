import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PersonPictureInter
from GuiHelper import GuiHelper
import sqlitepersist as sqp

class ExportDataDialog(gg.gExportDataDialog):
    def __init__(self, parent, fact : sqp.SQFactory):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        
    def _fill_gui(self):
        pass
    
    def showmodal(self):
        self._fill_gui()
        res = self.ShowModal()

        return res