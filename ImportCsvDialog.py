import os
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, SexCat, FluffyMonthCat, PersonPictureInter, FullPerson
import sqlitepersist as sqp
from GuiHelper import GuiHelper
import backgroundworkers as bgw

class ImportCsvDialog(gg.gImportCsvDialog):
    
    def __init__(self, parent, fact, zippath=None):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._zipfile = None
        self._worker = None
        self._zipfile = zippath
        self._docarchive = parent._docarchive
        self._targdir = None

        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)

    @property
    def haszip(self):
        return self._zipfile is not None
    
    @property
    def isrunning(self):
        return self._worker is not None and self._worker.isalive()
    
    def workerfinished(self, event):
        GuiHelper.enable_ctrls(True, self.m_startBU)
        GuiHelper.enable_ctrls(False, self.m_abortBU)

    def notifyperc(self, event):
        perc = event.data
        GuiHelper.set_val(self.m_importStateGAUGE, perc)

    def _filldialog(self):
        GuiHelper.enable_ctrls(self.haszip, self.m_startBU)
        GuiHelper.enable_ctrls(False, self.m_startBU)

    def showmodal(self):
        self._filldialog()
        return self.ShowModal()
    
    def fileChanged(self, event):
        zf = GuiHelper.get_val(self.m_zipfileFP)
        root, ext = os.path.splitext(zf)

        if ext is not None and ext == ".zip":
            if os.path.exists(zf):
                self._zipfile = zf
            else:
                self._zipfile = None
        else:
            self._zipfile = None

        GuiHelper.enable_ctrls(self.haszip, self.m_startBU)
        

    def startImport(self, event):
        paras = bgw.BgCsvImporterParas(self._fact, self._zipfile, self._docarchive)
        self._worker = bgw.BgCsvImporter(self, paras)
        self._worker.start()
        GuiHelper.enable_ctrls(False, self.m_startBU)
        GuiHelper.enable_ctrls(True, self.m_abortBU)

    def abortImport(self, event):
        self._worker.requestabort()