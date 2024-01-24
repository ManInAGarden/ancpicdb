import GeneratedGUI as gg
import wx
from GuiHelper import GuiHelper
from PersistClasses import Document, DocTypeCat, Person, Picture
import sqlitepersist as sqp
from Checkers import DocumentChecker, PictureChecker, PersonChecker

class DataCheckerDialog(gg.gDataCheckerDialog):
    def __init__(self, parent, fact):
        super().__init__(parent)
        self._fact = fact
        self._configuration = parent.configuration

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        pass

    def _check_pictures(self):
        allmessages = {"Bilder":None, "Dokumente":None, "Personen":None}
        pc = PictureChecker(self._fact)
        allmessages["Bilder"] = pc.do_checks()
        
        GuiHelper.add_nodes(self.m_chkResultsTCTR, allmessages)
        
    def doStartChecks(self, event):
        self._check_pictures()