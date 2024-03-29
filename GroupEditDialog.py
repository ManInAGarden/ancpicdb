import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PersistClasses import DataGroup, GroupTypeCat
import sqlitepersist as sqp

class GroupEditDialog(gg.gGroupEditDialog):
    @property
    def configuration(self):
        return self._configuration
    
    @property 
    def group(self):
        return self._group
    
    def _init_grouptypes(self):
        q = sqp.SQQuery(self._fact, GroupTypeCat).where(GroupTypeCat.LangCode=="DEU").order_by(GroupTypeCat.Value)
        self._grouptypes = q.as_list()

    def _get_catdisplay_list(self, vals : sqp.PCatalog):
        answ = []
        for val in vals:
            valstr = val.value
            answ.append(valstr)

        return answ
    
    def __init__(self, parent, fact, conf, grp):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._configuration = conf
        self._group = grp
        self._init_grouptypes()

    def _filldialog(self):
        g = self._group
        #self.m_typeCB.Set(self._get_catdisplay_list(self._grouptypes))
        GuiHelper.set_val(self.m_typeCB, g.grouptype, self._grouptypes)
        GuiHelper.set_val(self.m_nameTB, g.name)
        GuiHelper.set_val(self.m_orderNumberSPCTRL, g.ordernum)

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def editok(self, event):
        self._group.grouptype = GuiHelper.get_val(self.m_typeCB, self._grouptypes)
        self._group.name = GuiHelper.get_val(self.m_nameTB)
        self._group.ordernum = GuiHelper.get_val(self.m_orderNumberSPCTRL)
        self.EndModal(wx.ID_OK)