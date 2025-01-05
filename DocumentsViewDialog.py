from datetime import datetime
import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PersistClasses import Document, DocTypeCat
import sqlitepersist as sqp
from ConfigReader import ConfigReader
from EditDocumentDialog import EditDocumentDialog

class DocumentsViewDialog(gg.gDocumentsViewDialog):
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

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        """fill dialog with all the pictures"""
        q = sqp.SQQuery(self._fact, Document).order_by(Document.ScanDate)
        self._documents = list(q)
        docstrs = []

        for doc in self._documents:
            docstrs.append(doc.__str__())

        self.m_documentsLB.Clear()
        self.m_documentsLB.AppendItems(docstrs)

    def _create_readid(self):
        dt = datetime.now()
        return "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self.machlabel, dt)

    def addNewRow(self, event):
        readid = self._create_readid()
        doc = Document(readableid=readid)
        doc.type = self._fact.getcat(DocTypeCat, "NSP") #initialse as unspecified
        self._fact.flush(doc)
        self._documents.append(doc)
        self.m_documentsLB.Append(doc.__str__())
        self.m_documentsLB.Select(len(self._documents) - 1)

    def removeRow(self, event):
        seldoc, seldocpos = GuiHelper.get_selected_fromlb(self.m_documentsLB, self._documents)

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
        self.m_documentsLB.Delete(seldocpos)

    def editElement(self, event):
        seldoc, seldocpos = GuiHelper.get_selected_fromlb(self.m_documentsLB, self._documents)

        if seldoc is None:
            return
        
        dial = EditDocumentDialog(self, self._fact, seldoc)
        res = dial.showmodal()
        if res == wx.ID_CANCEL:
            return
        
        self._filldialog()
        