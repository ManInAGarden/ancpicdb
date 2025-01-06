import os
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PictureInfoBit, PersonPictureInter
import sqlitepersist as sqp
from GuiHelper import GuiHelper
import backgroundworkers as bgw
from ConfigReader import ConfigReader


class NewDbDialog(gg.gNewDbDialg) :
    
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive

    def __init__(self, parent, fact, spath, dbname):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self.logger = parent.logger
        self.storagepath = spath
        self.currdbname = dbname

        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)

        

    def _filldialog(self):
        return

    def showmodal(self):
        self._filldialog()

        return self.ShowModal() 
    

    def workerfinished(self, event):
        GuiHelper.enable_ctrls(True, self.m_createDbBU, self.m_cancelBU)

    def notifyperc(self, event):
        perc = event.data
        if perc < 0:
            GuiHelper.pulse(self.m_execuringG)
        else:
            GuiHelper.set_val(self.m_execuringG, perc)

    def createNewDbNow(self, event):
        newdbname = GuiHelper.get_val(self.m_newNameTB)
        copyold = GuiHelper.get_val(self.m_copyOldCB)
        
        targp = os.path.join(self.storagepath, newdbname)
        if os.path.exists(targp):
            GuiHelper.show_error("Eine Datenbank dieses Namens existiert bereits. Bitte wähle einen anderen Namen oder lösche die existierende Datenbank.")
            return

        paras = bgw.DbCreatorParas(self.storagepath, newdbname, copyold, self.currdbname)
        worker = bgw.BgDBCreator(self, self._configuration, self.logger, paras)
        worker.start()

        GuiHelper.enable_ctrls(False, self.m_createDbBU, self.m_cancelBU)

    
    def cancelNewDbCeation(self, event):
        self.EndModal(wx.ID_CANCEL)
