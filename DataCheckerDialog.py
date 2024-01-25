import GeneratedGUI as gg
import wx
from GuiHelper import GuiHelper
from PersistClasses import Document, DocTypeCat, Person, Picture, FullPerson
import sqlitepersist as sqp
from Checkers import DocumentChecker, PictureChecker, PersonChecker
from EditPictureDialog import EditPictureDialog
from PersonEditDialog import PersonEditDialog

class DataCheckerDialog(gg.gDataCheckerDialog):

    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive
    
    def __init__(self, parent, fact):
        super().__init__(parent)
        self._fact = fact
        self._configuration = parent.configuration
        self._docarchive = parent.docarchive

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        pass

    def _open_picture_dialog(self, pic : Picture):
        """Open a picture dialog, returns new data item when it  has been updated, None otherwise"""
        picdial = EditPictureDialog(self, self._fact, pic)
        res = picdial.showmodal()
        answ = None
        if res == wx.ID_OK:
            answ = picdial.picture
            self._fact.flush(answ)

        return answ


    def _open_person_dialog(self, pers : Person):
        """Open a picture dialog, returns new data item when it  has been updated, None otherwise"""
        persdial = PersonEditDialog(self, self._fact, pers)
        res = persdial.showmodal()
        answ = None
        if res == wx.ID_OK:
            answ = persdial.flushnget()

        return answ


    def _check_pictures(self, allmessages):
        pc = PictureChecker(self._fact)
        allmessages["Bilder"] = pc.do_checks()
        
    def _check_persons(self, allmessages):
        pc = PersonChecker(self._fact)
        allmessages["Personen"] = pc.do_checks()

    def _check_documents(self, allmessages):
        pass

    def doStartChecks(self, event):
        self.m_chkResultsTCTR.DeleteAllItems()

        #allmessages = {"Bilder":None, "Dokumente":None, "Personen":None}
        allmessages = {}

        if self.m_picturesCB.GetValue() == True:
            self._check_pictures(allmessages)
        if self.m_personsCB.GetValue() == True:
            self._check_persons(allmessages)
        if self.m_documentsCB.GetValue() == True:
            self._check_documents(allmessages)

        GuiHelper.add_nodes(self.m_chkResultsTCTR, allmessages)


    def errorTreeItemActivated(self, event):
        selid = self.m_chkResultsTCTR.GetSelection()
        dta = self.m_chkResultsTCTR.GetItemData(selid)

        if dta is None:
            return
        
        dtype = type(dta)
        if dtype == Picture:
            updpic = self._open_picture_dialog(dta)
            if updpic is not None:
                self.m_chkResultsTCTR.SetItemData(selid, updpic)
        elif dtype == FullPerson:
            updpers = self._open_person_dialog(dta)
            if updpers is not None:
                self.m_chkResultsTCTR.SetItemData(selid, updpers)
        else:
            GuiHelper.show_error("Unbekannter Datentyp <{}> im TreeView",
                                 dtype.__name__)
            
        dta = None #free data, wonder if that really works
