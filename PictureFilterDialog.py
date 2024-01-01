import copy
from dateutil.relativedelta import relativedelta
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, SexCat
import sqlitepersist as sqp
from GuiHelper import GuiHelper


class PictureFilterDialog(gg.gPictureFilterDialog):
    
    @property
    def filter(self):
        return self._filter
    
    def __init__(self, parent, fact, dta):
        super().__init__(parent)
        self._fact = fact
        self._filter = copy.copy(dta) #calling dialog keeps an independent version of this, so we need a copy

    def _fill_dialog(self):
        f = self._filter
        GuiHelper.set_val(self.m_titelTB, f.title)
        GuiHelper.set_val(self.m_kennummerTB, f.kennummer)
        GuiHelper.set_val(self.m_dayTB, f.daytaken)
        GuiHelper.set_val(self.m_monthTB, f.monthtaken)
        GuiHelper.set_val(self.m_yearTB, f.yeartaken)

    def _fill_filterdata(self):
        f = self._filter
        f.title = GuiHelper.get_val(self.m_titelTB)
        f.kennummer = GuiHelper.get_val(self.m_kennummerTB)
        f.daytaken = GuiHelper.get_val(self.m_dayTB)
        f.monthtaken = GuiHelper.get_val(self.m_monthTB)
        f.yeartaken = GuiHelper.get_val(self.m_yearTB)

    def showmodal(self):
        self._fill_dialog()
        answ = self.ShowModal()
        if answ == wx.ID_CANCEL: return answ
        self._fill_filterdata()
        return answ