import wx
import wx.adv

import sqlitepersist as sqp
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PersistClasses import Person

class FindPersonsDialog(gg.gFindPersonsDialog):
    PERSONDEFINS = [
        {"propname" : "firstname", "title": "Vorname", "width":120},
        {"propname" : "name", "title": "Nachname", "width":120},
        {"propname" : "cons_birth_year", "title": "Geburtsjahr", "width":120}
    ]

    @property
    def selected(self):
        return self._selected
    
    def __init__(self, parent, fact, excludeids):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._selected = None
        self._allpersons = []
        self._filterexp = None
        self._excludethese_ids = excludeids
        self._init_gui()

    def _init_gui(self):
        GuiHelper.set_columns_forlstctrl(self.m_searchResultLCTRL,
                                         self.PERSONDEFINS)
        
    def _fill_gui(self):
        exp1 = sqp.NotIsIn(Person.Id, self._excludethese_ids)
        if self._filterexp is not None:
            exp = (exp1) & (self._filterexp)
        else:
            exp = exp1

        self._allpersons = sqp.SQQuery(self._fact, Person).where(exp).order_by(Person.Name, Person.FirstName).as_list()
        GuiHelper.set_data_for_lstctrl(self.m_searchResultLCTRL, 
                                       self.PERSONDEFINS,
                                       self._allpersons)
        
    def showmodal(self):
        self._fill_gui()
        res = self.ShowModal()

        if res == wx.ID_CANCEL: 
            self._selected = None
            return res

        self._selected = GuiHelper.get_all_selected_fromlctrl(self.m_searchResultLCTRL, self._allpersons)
        if self._selected is not None and len(self._selected)==0:
            self._selected = None
            return wx.ID_CANCEL
        else:
            return res

    def _isempty(self, val :str):
        if val is None:
            return True
        if len(val)==0:
            return True
        
        return val.isspace()
    
    def doSearch(self, event):
        sfirstname = GuiHelper.get_val(self.m_firstNameTB)
        sname = GuiHelper.get_val(self.m_nameTB)

        self._filterexp = None
        if not self._isempty(sfirstname):
            if not sfirstname.endswith("*"):
                sfirstname += "*"
            self._filterexp = (sqp.IsLike(Person.FirstName, sfirstname.replace("*", "%")))
        
        if not self._isempty(sname):
            if not sname.endswith("*"):
                sname += "*"
            subexp = (sqp.IsLike(Person.Name, sname.replace("*", "%")))
            if self._filterexp is None:
                self._filterexp = subexp
            else:
                self._filterexp = (self._filterexp) & (subexp)

        self._fill_gui()

    