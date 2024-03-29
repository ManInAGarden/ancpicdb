import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PersonPictureInter
from GuiHelper import GuiHelper
import sqlitepersist as sqp

class EditSignifcPictureDialog(gg.gEditSignifcPictureDialog):
    @property
    def picinter(self):
        return self._picinter
    
    def __init__(self, parent, fact : sqp.SQFactory, picinter : PersonPictureInter):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._picinter = picinter
        
    def _fill_gui(self):
        pi = self._picinter
        GuiHelper.set_val(self.m_kennungTB, pi.picture.readableid)
        GuiHelper.set_val(self.m_titleTB, pi.picture.title)
        GuiHelper.set_val(self.m_positionSPC, pi.position)
        GuiHelper.set_val(self.m_subtitleTB, pi.subtitle)

    def showmodal(self):
        self._fill_gui()
        res = self.ShowModal()
        if res != wx.ID_OK:
            return
        
        pi = self._picinter
        pi.position = GuiHelper.get_val(self.m_positionSPC)
        pi.subtitle = GuiHelper.get_val(self.m_subtitleTB)

        self._fact.flush(pi)

        return res
    
    