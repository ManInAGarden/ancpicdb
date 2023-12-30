import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PersistClasses import DataGroup, GroupTypeCat
import sqlitepersist as sqp
from ConfigReader import ConfigReader
from GroupEditDialog import GroupEditDialog

class GroupsViewDialog(gg.gGroupsDialog):
    @property
    def configuration(self):
        return self._configuration
    
    def __init__(self, parent, fact, conf):
        super().__init__(parent)
        self._fact = fact
        self._configuration = conf
        self._create_grlist_cols()

    def _create_grlist_cols(self):
        self.m_groupsLCTRL.InsertColumn(0, "Gruppentyp")
        self.m_groupsLCTRL.InsertColumn(1, "Bezeichnung")
        self.m_groupsLCTRL.InsertColumn(2, "Ordnungszahl")

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _ess(self, val):
        if val is None: return ""

        return val.__str__()
    
    
    def _ecs(self, val):
        if val is None: return ""

        return val.value
    
    def _add_grline(self, dataidx,  grp : DataGroup):
        lct = self.m_groupsLCTRL
        colc = lct.GetColumnCount()
        idx = lct.InsertItem(colc, self._ecs(grp.grouptype))
        lct.SetItemData(idx, dataidx)
        lct.SetItem(idx, 1, self._ess(grp.name))
        lct.SetItem(idx, 2, self._ess(grp.ordernum))

    def _fill_grcols(self):
        self.m_groupsLCTRL.DeleteAllItems()
        if self._groups is None: return

        idx = 0
        for grp in self._groups:
            self._add_grline(idx, grp)
            idx += 1

    def _filldialog(self):
        """fill dialog with all groups found in the database"""
        q = sqp.SQQuery(self._fact, DataGroup).order_by(DataGroup.GroupType)
        self._groups = list(q)
        self._fill_grcols()

    def addNewGroup(self, event):
        grp = DataGroup(name="<neue Gruppe>")
        self._fact.flush(grp)
        self._groups.append(grp)
        idx = len(self._groups) - 1
        self._add_grline(idx, grp)

    def _get_grp_idx(self, sgrp):
        if self._groups is None: return -1

        idx = 0
        for grp in self._groups:
            if grp._id == sgrp._id:
                return idx
            idx += 1

        return -1
    
    def removeGroup(self, event):
        selgrp = GuiHelper.get_selected_fromlctrl(self.m_groupsLCTRL, self._groups)

        if selgrp is None:
            return
        
        if selgrp.name is not None:
            name = selgrp.name
        else:
            name = "kein Name"

        res = wx.MessageBox("Soll die Gruppe <{}> tatsächlich gelöscht werden?".format(name),
                            "Rückfrage",
                            style=wx.YES_NO)
        
        if res != wx.YES:
            return 

        # delete in database        
        self._fact.delete(selgrp)
        
        #refill cache and gui
        self._filldialog()

    def editGroup(self, event):
        grp = GuiHelper.get_selected_fromlctrl(self.m_groupsLCTRL, self._groups)
        grpdial = GroupEditDialog(self, self._fact, self._configuration, grp)

        res = grpdial.showmodal()

        if res != wx.ID_OK:
            return
        
        edigrp = grpdial.group
        self._fact.flush(edigrp)
        self._filldialog()
        
