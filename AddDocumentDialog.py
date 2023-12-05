import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, Document
from GuiHelper import GuiHelper
import sqlitepersist as sqp

class AddDocumentDialog(gg.gAddDocumentDialog):
    
    @property
    def person(self):
        return self._person
    
    @property
    def selection(self):
        return self._selection
    
    def __init__(self, parent, fact : sqp.SQFactory, person : Person):
        super().__init__(parent)
        if person is None:
            raise Exception("Es muss eine Person benutzt werden! Person ist None!")
        self._fact = fact
        self._configuration = parent._configuration
        self._person = person
        self._selection = []

    def _init_gui(self):
        
        self.m_documentsLCTRL.ClearAll()
        self.m_documentsLCTRL.InsertColumn(0, "Kennung")
        self.m_documentsLCTRL.InsertColumn(1, "Titel")
        self.m_documentsLCTRL.InsertColumn(2, "Produziert am")
        self.m_documentsLCTRL.InsertColumn(3, "Dokumenttyp")
        self.m_documentsLCTRL.InsertColumn(4, "Gescannt am")

    def _asds(self, dt):
        if dt is None:
            return ""
        
        return "{:%d.%m.%Y}".format(dt)

    def _catval(self, cat):
        if cat is None:
            return None
        return cat.value
    
    def _fill_dialog(self):
        #find all those documents that have not been connected to the current person
        
        q = sqp.SQQuery(self._fact, Document).order_by(sqp.OrderInfo(Document.Created, sqp.OrderDirection.DESCENDING))

        ct = 0
        self._docdata = []
        for pdoc in q:
            if ct >= 100:
                break
            
            self._docdata.append(pdoc)

            idx = self.m_documentsLCTRL.InsertItem(self.m_documentsLCTRL.GetColumnCount(), pdoc.readableid)
            self.m_documentsLCTRL.SetItemData(idx, ct)
            self.m_documentsLCTRL.SetItem(idx, 0, pdoc.readableid)
            self.m_documentsLCTRL.SetItem(idx, 1, pdoc.title)
            self.m_documentsLCTRL.SetItem(idx, 2, self._asds(pdoc.productiondate))
            self.m_documentsLCTRL.SetItem(idx, 3, self._catval(pdoc.type))
            self.m_documentsLCTRL.SetItem(idx, 4, self._asds(pdoc.scandate))
            ct += 1

    def showmodal(self):
        self._init_gui()
        self._fill_dialog()
        res = self.ShowModal()
        if res is wx.ID_CANCEL:
            self._selection = []
            return res
        
        selidx = self.m_documentsLCTRL.GetFirstSelected()
        if selidx == -1:
            return res
        
        while(selidx != -1):
            docpos = self.m_documentsLCTRL.GetItemData(selidx)
            self._selection.append(self._docdata[docpos])
            selidx = self.m_documentsLCTRL.GetNextSelected(selidx)

        return res