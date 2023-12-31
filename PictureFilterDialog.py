import datetime
from dateutil.relativedelta import relativedelta
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, SexCat
import sqlitepersist as sqp
from GuiHelper import GuiHelper


class PictureFilterDialog(gg.gPictureFilterDialog):
    
    def __init__(self, parent, fact, dta):
        super().__init__(parent)
        self._fact = fact
        self._filter = dta

    def _fill_dialog(self):
        f = self._filter
        GuiHelper.set_val(self.m_titelTB, f.title)
        GuiHelper.set_val(self.m_kennummerTB, f.kennummer)
        GuiHelper.set_val(self.m_dayTB, f.daytaken)
        GuiHelper.set_val(self.m_monthTB, f.monthtaken)
        GuiHelper.set_val(self.m_yearTB, f.yeartaken)

    def _fill_filterdata(self):
        pass

    def showmodal(self):
        self._fill_dialog()
        answ = self.ShowModal()
        if answ == wx.ID_CANCEL: return answ
        self._fill_filterdata()
        return answ