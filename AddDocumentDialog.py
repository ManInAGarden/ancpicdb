import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, Document
from GuiHelper import GuiHelper
import sqlitepersist as sqp


class DocumentSelectionFilter:
    def __init__(self):
        self.title = None
        self.productiondate = None
        self.datescanned = None
        self.kennung = None
        self.prductiondateop = None
        self.datescannedop = None

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
    
    def _get_current_filter(self) -> DocumentSelectionFilter:
        opl = ["=", ">", "<"]
        answ = DocumentSelectionFilter()
        answ.title = GuiHelper.get_val(self.m_titleTB)
        answ.kennung = GuiHelper.get_val(self.m_kennungTB)
        answ.productiondate = GuiHelper.get_val(self.m_productionDateDP)
        answ.productiondateop = GuiHelper.get_val(self.m_productionDateOperatorCB, opl)
        answ.scandate = GuiHelper.get_val(self.m_scanDateDP)
        answ.scandateop = GuiHelper.get_val(self.m_scandateOperatorCB, opl)

        return answ

    def _catval(self, cat):
        if cat is None:
            return None
        return cat.value
    
    def _add2exp(self, exp, newpart):
        if exp is None: 
            return newpart

        return (exp) & (newpart)
    
    def _get_current_expr(self, pf : DocumentSelectionFilter):
        answ = None
        if is_strict(pf.kennung):
            answ = Document.ReadableId == pf.kennung
            return answ
        elif is_def(pf.kennung):
            answ = sqp.IsLike(Document.ReadableId, pf.kennung.replace("*", "%"))

        if is_strict(pf.title):
            answ = self._add2exp(answ, Document.Title==pf.title)
        elif is_def(pf.title):
            answ = self._add2exp(answ, sqp.IsLike(Document.Title, pf.title.replace("*", "%")))

        if pf.productiondate is not None:
            if pf.productiondateop == "=":
                answ = self._add2exp(answ, Document.ProductionDate == pf.productiondate)
            elif pf.productiondateop == ">":
                answ = self._add2exp(answ, Document.ProductionDate > pf.productiondate)
            elif pf.productiondateop == "<":
                answ = self._add2exp(answ, Document.ProductionDate < pf.productiondate)

        if pf.scandate is not None:
            if pf.scandateop == "=":
                answ = self._add2exp(answ, Document.ScanDate == pf.scandate)
            elif pf.scandateop == ">":
                answ = self._add2exp(answ, Document.ScanDate > pf.scandate)
            elif pf.scandateop == "<":
                answ = self._add2exp(answ, Document.ScanDate < pf.scandate)

        return answ
    
    def _fill_dialog(self):
        #find all those documents that have not been connected to the current person, additionally try to set a filter
        self._fact.fill_joins(self._person, Person.Documents) #get any already connected docs for the person
        alreadycondocs = list(map(lambda docinter: docinter.documentid, self._person.documents))

        f = self._get_current_filter()
        exp = self._get_current_expr(f)

        q = sqp.SQQuery(self._fact, Document).where(exp).order_by(sqp.OrderInfo(Document.Created, sqp.OrderDirection.DESCENDING))

        ct = 0
        self._docdata = []
        self.m_documentsLCTRL.DeleteAllItems()
        for pdoc in q:
            if ct >= 100:
                break
            
            if not pdoc._id in alreadycondocs:
                self._docdata.append(pdoc)

                try:
                    idx = self.m_documentsLCTRL.InsertItem(self.m_documentsLCTRL.GetColumnCount(), pdoc.readableid)
                    self.m_documentsLCTRL.SetItemData(idx, ct)
                    self.m_documentsLCTRL.SetItem(idx, 0, pdoc.readableid)
                    self.m_documentsLCTRL.SetItem(idx, 1, pdoc.title)
                    self.m_documentsLCTRL.SetItem(idx, 2, self._asds(pdoc.productiondate))
                    self.m_documentsLCTRL.SetItem(idx, 3, self._catval(pdoc.type))
                    self.m_documentsLCTRL.SetItem(idx, 4, self._asds(pdoc.scandate))
                except Exception as exc:
                    pass
                
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
    
    def applyFilter(self, event):
        self._fill_dialog()

    #module defs
def is_def(val : str) -> bool:
    return val is not None and len(val) > 0

def is_strict(val : str) -> bool:
    if not is_def(val):
        return False
    
    return not "*" in val