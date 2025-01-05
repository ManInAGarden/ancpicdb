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
                      {"title": "Archvierungs-Id", "width": 140, "propname":"readableid" },
                      {"title": "angelegt", "width": 50, "propname":"created" },
                      {"title": "letzte Änderung", "width": 50, "propname":"lastupdate" },
                      {"title": "mit DB", "width": 10, "propname":"hasdb" },
                      {"title": "mit Archiv", "width": 10, "propname":"hasarchive"},
                      {"title": "Ablageort", "width": 300, "propname":"location"}
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
        