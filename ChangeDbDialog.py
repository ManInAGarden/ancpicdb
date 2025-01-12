import os
import GeneratedGUI as gg
import wx
from GuiHelper import GuiHelper
from DatabaseRepres import DatabaseRepres


class ChangeDbDialog(gg.mChangeDbDialog):
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive
    
    @property
    def selected_dblocation(self) -> str:
        if self._selected_dbrep is None:
            return None
        else:
            return self._selected_dbrep.location
    
    @property
    def selected_dbname(self) -> str:
        if self._selected_dbrep is None:
            return None
        else:
            return self._selected_dbrep.name
    
    
    
    def __init__(self, parent, storagepath, dbname):
        super().__init__(parent)
        GuiHelper.set_icon(self)
        self._configuration = parent.configuration
        self._docarchive = parent.docarchive
        self._selected_dbrep = None

        self._storagepath = storagepath
        self._dbname = dbname
        self._configuration = parent.configuration

        # set the columdefinitions
        self._dblistdefins =  [
                      {"title": "Name", "width": 100, "propname":"name" },
                      {"title": "Angelegt am", "width": 100, "propname":"created" },
                      {"title": "Mit DB", "width": 50, "propname":"hasdb" },
                      {"title": "Mit Archiv", "width": 50, "propname":"hasarchive"},
                      {"title": "Ablageort", "width": wx.LIST_AUTOSIZE_USEHEADER, "propname":"location"}
                    ]



    def showmodal(self):
        self._filldialog()
        return self.ShowModal()
    

    def _filldialog(self):
        self._founddatabases = self._getalldatabases()
        GuiHelper.set_columns_forlstctrl(self.mDatabasesLBCTRL, 
                                         self._dblistdefins)
        
        GuiHelper.set_data_for_lstctrl(self.mDatabasesLBCTRL,
                                       self._dblistdefins,
                                       self._founddatabases)

        self.mDatabasesLBCTRL.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.mDatabasesLBCTRL.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.mDatabasesLBCTRL.SetColumnWidth(4, wx.LIST_AUTOSIZE)

    def _getalldatabases(self):
        dbs = []
        for elem in os.listdir(self._storagepath):
            dirp = os.path.join(self._storagepath, elem)
            if os.path.isdir(dirp):
                db = DatabaseRepres(elem, dirp)
                dbs.append(db)

        return dbs


    def OnDatabaseSelected(self, event):
        seldbrep = GuiHelper.get_selected_fromlctrl(self.mDatabasesLBCTRL, self._founddatabases)
        self._selected_dbrep = seldbrep

    def OnDatabaseActivated(self, event):
        seldbrep = GuiHelper.get_selected_fromlctrl(self.mDatabasesLBCTRL, self._founddatabases)
        self._selected_dbrep = seldbrep

        answ = GuiHelper.ask_user(self, "Möchtest du zur Datenbank <{}> wechseln?".format(self.selected_dbname))
        if answ == wx.ID_YES:
            self.EndModal(wx.ID_OK)