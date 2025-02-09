import copy
import GeneratedGUI as gg
from GuiHelper import GuiHelper
import sqlitepersist as sqp
import wx
import wx.adv
from PersistClasses import GroupTypeCat, DocTypeCat, DataGroup

class DocumentFilterDialog(gg.gDocumentFilterDialog):
    
    def __init__(self, parent, fact, dta):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._filter = copy.copy(dta) #calling dialog keeps an independent version of this, so we need a copy
        self._get_all_pgroups()
        self._get_all_doctypes()

    @property
    def filter(self):
        return self._filter
    
    def grouppres(self, grp) -> str:
        return grp.name
    
    def doctres(self, doct) -> str:
        return doct.value

    def _get_all_pgroups(self):
        self._groups = sqp.SQQuery(self._fact, DataGroup).where(DataGroup.GroupType=="DOC").as_list()


    def _get_all_doctypes(self):
        self._doctypes = sqp.SQQuery(self._fact,
                                     DocTypeCat).where(DocTypeCat.LangCode=="DEU").order_by(DocTypeCat.Value).as_list()
        self._fact


    def _fill_dialog(self):
        f = self._filter
        GuiHelper.set_val(self.m_titelTB, f.title)
        GuiHelper.set_val(self.m_kennummerTB, f.kennummer)
        GuiHelper.set_sqp_objval(self.m_groupCB, f.gruppe, self.grouppres, self._groups)
        GuiHelper.set_sqp_objval(self.m_docTypeCB, f.doctype, self.doctres, self._doctypes)
        GuiHelper.set_val(self.m_prodDateDP, f.proddate)

    def _fill_filterdata(self):
        f = self._filter
        f.title = GuiHelper.get_val(self.m_titelTB)
        f.kennummer = GuiHelper.get_val(self.m_kennummerTB)
        f.proddate = GuiHelper.get_val(self.m_prodDateDP)
        f.gruppe = GuiHelper.get_sqp_objval(self.m_groupCB, self._groups)
        f.doctype = GuiHelper.get_sqp_objval(self.m_docTypeCB, self._doctypes)

    def showmodal(self) -> int:
        self._fill_dialog()
        answ = self.ShowModal()
        if answ == wx.ID_CANCEL: return answ
        self._fill_filterdata()
        return answ