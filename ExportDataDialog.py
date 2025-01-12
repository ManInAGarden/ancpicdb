import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PersonPictureInter
from GuiHelper import GuiHelper
import sqlitepersist as sqp
import datetime as dt
import backgroundworkers as bgw

class CsvExportSettings:
    DOPERSONS = 1
    DOPICTURES = 2
    DODOCUMENTS = 4

    @property
    def targetdir(self):
        return self._targetDir
    
    @targetdir.setter
    def targetdir(self, val):
        self._targetDir = val

    @property
    def changed_after(self):
        return self._changedAfter
    
    @changed_after.setter
    def changed_after(self, val):
        self._changedAfter = val

    @property
    def exp_properties(self):
        return self._expproperties
    
    @exp_properties.setter
    def exp_properties(self, val):
        self._expproperties = val

    @property
    def dopersons(self):
        inter = self._expproperties & self.DOPERSONS 
        return inter == self.DOPERSONS

    @property
    def dopictures(self):
        return self._expproperties & self.DOPICTURES == self.DOPICTURES
    
    @property
    def dodocuments(self):
        return self._expproperties & self.DODOCUMENTS == self.DODOCUMENTS

    def __init__(self):
        self._targetDir = None
        self._changedAfter = None
        self._expproperties = self.DOPERSONS | self.DOPICTURES | self.DODOCUMENTS



class ExportDataDialog(gg.gExportDataDialog):

    @property
    def csvexpsettings(self):
        if self._data is None:
            answ = CsvExportSettings()
        else:
            answ = self._data

        return answ

    def __init__(self, parent, fact : sqp.SQFactory, data : CsvExportSettings):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._data = data
        self._bw = None
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self._machlabel = self._configuration.get_value("gui", "machlabel")
        if self._machlabel is None:
            self._machlabel = "XXXX"

        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)

    @property
    def havetarget(self):
        d = self._data
        if d.targetdir is None:
            return False
        
        if not type(d.targetdir) is str:
            return False
        
        return len(d.targetdir) > 0
    

    def _fill_gui(self):
        if self._data is None:
            return
        
        d = self._data
        GuiHelper.set_val(self.m_targetDIRP, d.targetdir)
        GuiHelper.set_val(self.m_onlyNewerThanDPI, d.changed_after)
        GuiHelper.set_val(self.m_personsCB, d.dopersons)
        GuiHelper.set_val(self.m_documentsCB, d.dodocuments)
        GuiHelper.set_val(self.m_picturesCB, d.dopictures)
        
        self.m_startExportBU.Enable(self.havetarget)
    
    def showmodal(self):
        self._fill_gui()
        res = self.ShowModal()

        return res
    
    def targetDirChanged(self, event):
        self._data.targetdir = GuiHelper.get_val(self.m_targetDIRP)
        self.m_startExportBU.Enable(self.havetarget)

    def add_prop(self, prop):
        self._data.exp_properties = self._data.exp_properties | prop

    def workerfinished(self, event : bgw.ResultEvent):
        succ = event.success
        ct = event.data
        if succ:
            GuiHelper.set_val(self.m_bgresultTB, "{} Datenelemente wurden exportiert".format(ct))
        else:
            GuiHelper.set_val(self.m_bgresultTB, "Misserfolg! Daten wurde nicht exportiert")

        GuiHelper.enable_ctrls(True, self.m_startExportBU)
        GuiHelper.enable_ctrls(False, self.m_abortExportBU)

    def notifyperc(self, event):
        perc = event.data
        self.m_workDoneGAUGE.SetValue(perc)
        GuiHelper.set_val(self.m_bgresultTB, "Datenexport läuft")

    def doClose(self, event):

        if self._bw is not None and self._bw.is_alive():
            GuiHelper.show_message("Bitte warte bis der Hintergrundjob für den Export beendet ist")
            return
        
        d = self._data
        d.targetdir = GuiHelper.get_val(self.m_targetDIRP)
        d.changed_after = GuiHelper.get_val(self.m_onlyNewerThanDPI)
        
        d.exp_properties = 0
        if GuiHelper.get_val(self.m_personsCB):
            self.add_prop(CsvExportSettings.DOPERSONS)
        if GuiHelper.get_val(self.m_picturesCB):
            self.add_prop(CsvExportSettings.DOPICTURES)
        if GuiHelper.get_val(self.m_documentsCB):
            self.add_prop(CsvExportSettings.DODOCUMENTS)

        self.EndModal(wx.ID_OK)

    def doCloseDialog(self, event):
        return
    
    def startCsvExport(self, event):
        targetdir = GuiHelper.get_val(self.m_targetDIRP)
        changed_after = GuiHelper.get_val(self.m_onlyNewerThanDPI)
        
        dopers = GuiHelper.get_val(self.m_personsCB)
        dopics = GuiHelper.get_val(self.m_picturesCB)
        dodocs = GuiHelper.get_val(self.m_documentsCB)
        paras = bgw.BgCsvExtractorParas(self._fact, 
                                        targetdir,
                                        self._docarchive,
                                        self._machlabel,
                                        changed_after,
                                        dopers,
                                        dodocs,
                                        dopics)
       
        self._bw = bgw.BgCsvExtractor(notifywin=self, paras=paras)
        self._bw.start()
        GuiHelper.set_val(self.m_bgresultTB, "Datemexport gestartet")
        GuiHelper.enable_ctrls(False, self.m_startExportBU)
        GuiHelper.enable_ctrls(True, self.m_abortExportBU)

    def abortCsvExport(self, event):
        self._bw.requestabort()