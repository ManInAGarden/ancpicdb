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
    
    def __init__(self, parent, storagepath, dbname):
        super().__init__(parent)
        GuiHelper.set_icon(self)
        self._configuration = parent.configuration
        self._docarchive = parent.docarchive

        self._storagepath = storagepath
        self._dbname = dbname
        self._configuration = parent.configuration

        # set the columdefinitions
        self._dblistdefins =  [
                                 {"title": "Name", "width": 100, "propname":"name" },
                                 {"title": "angelegt", "width": 50, "propname":"created" },
                                 {"title": "mit DB", "width": 10, "propname":"hasdb" },
                                 {"title": "mit Archiv", "width": 10, "propname":"hasarchive"},
                                 {"title": "Ablageort", "width": 300, "propname":"location"}
                              ]

    def showmodal(self):
        self.selected_db = None
        self._filldialog()
        return self.ShowModal()
    

    def _filldialog(self):
        self._founddatabases = self._getalldatabases()
        GuiHelper.set_columns_forlstctrl(self.mDatabasesLBCTRL, 
                                         self._dblistdefins)
        
        GuiHelper.set_data_for_lstctrl(self.mDatabasesLBCTRL,
                                       self._dblistdefins,
                                       self._founddatabases)

    def _getalldatabases(self):
        dbs = []
        for elem in os.listdir(self._storagepath):
            dirp = os.path.join(self._storagepath, elem)
            if os.path.isdir(dirp):
                db = DatabaseRepres(elem, dirp)
                dbs.append(db)

        return dbs


    def OnDatabaseSelected(self, event):
        self.selected_db = GuiHelper.get_selected_fromlctrl(self.mDatabasesLBCTRL, self._founddatabases)
        