import datetime as dt

import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PathZipper import PathZipper
import backgroundworkers as bgw


class CreateBackupDialog(gg.gCreateBackupDialog):
    
    @property
    def hastargetdir(self):
        return self._targdir is not None and len(self._targdir) > 0
    
    def __init__(self, parent, fact, dbname):
        super().__init__(parent)
        
        GuiHelper.set_icon(self)

        self._bworker = None
        self._fact = fact
        self._configuration = parent.configuration
        self._docarchive = parent.docarchive
        self._logger = parent.logger
        self._targdir = None
        self._dbname = dbname

        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)


    def workerfinished(self, event):
        succ = event.success
        GuiHelper.enable_ctrls(True, self.m_startBackupBU)
        GuiHelper.enable_ctrls(False, self.m_cancelBackupBU)
        if succ:
            GuiHelper.set_val(self.m_statusTB, "Die Datenbank und das Dokumentarchiv wurden gemeinsam in ein Zip-File gesichert")
        else:
            GuiHelper.set_val(self.m_statusTB, "Fehlschlag bei der Sicherung!")

    def notifyperc(self, event):
        perc = event.data
        GuiHelper.set_val(self.m_backupGAUGE, perc)

    def showmodal(self):
        self._fill_gui()
        
        return self.ShowModal()
    
    def _fill_gui(self):
        GuiHelper.enable_ctrls(self.hastargetdir, self.m_startBackupBU)
        GuiHelper.enable_ctrls(False, self.m_cancelBackupBU)
        GuiHelper.set_val(self.m_statusTB, "")

    def targetDirChanged(self, event):
        tdir = GuiHelper.get_val(self.m_targetDirDP)
        self._targdir = tdir
        GuiHelper.enable_ctrls(self.hastargetdir, self.m_startBackupBU)


    def startBackup(self, event):
        if not self.hastargetdir: return
        
        paras = bgw.BgDbZipperParas(self._targdir, self._dbname)
        self._bworker = bgw.BgDbZipper(self, 
                                      self._configuration, 
                                      self._logger, 
                                      paras)
        
        self._bworker.start()
        GuiHelper.set_val(self.m_statusTB, "Sicherung wurde gestartet")
        GuiHelper.enable_ctrls(False, self.m_startBackupBU)
        GuiHelper.enable_ctrls(True, self.m_cancelBackupBU)
    
    def abortBackup(self, event):
        if self._bworker is None: return

        self._bworker.requestabort()                               