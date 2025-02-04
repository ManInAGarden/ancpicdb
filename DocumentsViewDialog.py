from datetime import datetime
import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PersistClasses import Document, DocTypeCat
import sqlitepersist as sqp
from ConfigReader import ConfigReader
from EditDocumentDialog import EditDocumentDialog
from ConnectedPersonsDialog import ConnectedPersonsDialog

class DocumentsViewDialog(gg.gDocumentsViewDialog):

    DOCLISTDEFINS=[
        {"propname" : "readableid", "title": "ID", "width":230},
        {"propname" : "scandate", "title": "Scandatum", "width":100, "format": "{:%d.%m.%Y}"},
        {"propname" : "productiondate", "title": "Erstelldatum", "width":100, "format": "{:%d.%m.%Y}"},
        {"propname" : "title", "title": "Titel", "width":380},
        #{"propname" : "groupname", "title": "Gruppe", "width":250},
        {"propname" : "ext", "title": "Typ", "width":40},
        {"propname" : "documentgroup.groupordername", "title": "Grp#", "width":60}
    ]
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive

    def __init__(self, parent, fact):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"



    def _prep_cols(self):
        GuiHelper.set_columns_forlstctrl(self.m_documentsLCTRL, self.DOCLISTDEFINS)
        
    def showmodal(self):
        self._prep_cols()
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        """fill dialog with all the pictures"""
        q = sqp.SQQuery(self._fact, Document).order_by(sqp.OrderInfo(Document.ScanDate, sqp.OrderDirection.DESCENDING))
        self._documents = list(q)

        GuiHelper.set_data_for_lstctrl(self.m_documentsLCTRL,
                                       self.DOCLISTDEFINS,
                                       self._documents)

    def _create_readid(self):
        dt = datetime.now()
        return "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self.machlabel, dt)

    def addNewRow(self, event):
        readid = self._create_readid()
        doc = Document(readableid=readid)
        doc.type = self._fact.getcat(DocTypeCat, "NSP") #initialise as unspecified
        self._fact.flush(doc)
        self._documents.append(doc)
        
        GuiHelper.append_data_for_lstctrl(self.m_documentsLCTRL,
                                          self.DOCLISTDEFINS,
                                          doc)

    def removeRow(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)

        if seldoc is None:
            return
        
        if seldoc.readableid is not None:
            name = seldoc.readableid
        elif seldoc.title is not None:
            name = seldoc.title
        else:
            name = "kein Name"

        res = wx.MessageBox("Soll das Dokument <{}> tatsächlich gelöscht werden?".format(name),
                            "Rückfrage",
                            style=wx.YES_NO)
        
        if res != wx.YES:
            return 
        
        self._fact.delete(seldoc)
        self._filldialog()

    def editElement(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
    
        if seldoc is None:
            return
        
        dial = EditDocumentDialog(self, self._fact, seldoc)
        res = dial.showmodal()
        if res == wx.ID_CANCEL:
            return
        
        self._filldialog()

    def downloadDocument(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)

        if seldoc is None: return
        

    def documentSelected(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        
        GuiHelper.enable_ctrls(seldoc != None, 
                                   self.m_downloadDocumentBU, 
                                   self.m_editBU,
                                   self.m_deleteDocumentBU,
                                   self.m_preparePrintBU,
                                   self.m_showConnectedPersonsBU)
        
    def documentDeselected(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        
        GuiHelper.enable_ctrls(seldoc != None, 
                                   self.m_downloadDocumentBU, 
                                   self.m_editBU,
                                   self.m_deleteDocumentBU,
                                   self.m_preparePrintBU,
                                   self.m_showConnectedPersonsBU)
        
    def showConnectedPersons(self, event):
        """display and edit the connections to persons of the selected document or to the first selected document
           if more than one is selected
        """
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        
        if seldoc is None: return

        conndial = ConnectedPersonsDialog(self, self._fact, seldoc)
        conndial.showmodal()