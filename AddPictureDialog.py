import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, Picture
from GuiHelper import GuiHelper
import sqlitepersist as sqp

class PictureSelectionFilter:
    def __init__(self):
        self.title = None
        self.datetaken = None
        self.datescanned = None
        self.kennung = None
        self.datetakenop = None
        self.datescannedop = None

class AddPictureDialog(gg.gAddPictureDialog):
    
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
        self.m_picturesLCTRL.ClearAll()
        self.m_picturesLCTRL.InsertColumn(0, "Kennung")
        self.m_picturesLCTRL.InsertColumn(1, "Titel")
        self.m_picturesLCTRL.InsertColumn(2, "Aufgenommen am")
        self.m_picturesLCTRL.InsertColumn(3, "Gescannt am")

    def _asds(self, dt):
        if dt is None:
            return ""
        
        return "{:%d.%m.%Y}".format(dt)

   
    def _add2exp(self, exp, newpart):
        if exp is None: 
            return newpart

        return (exp) & (newpart)
                
    def _get_current_filter(self) -> PictureSelectionFilter:
        opl = ["=", ">", "<"]
        answ = PictureSelectionFilter()
        answ.title = GuiHelper.get_val(self.m_titleTB)
        answ.kennung = GuiHelper.get_val(self.m_kennungTB)
        answ.datetaken = GuiHelper.get_val(self.m_dateTakenDP)
        answ.datetakenop = GuiHelper.get_val(self.m_operatorTakenCB, opl)
        answ.datescanned = GuiHelper.get_val(self.m_scanDateDP)
        answ.datescannedop = GuiHelper.get_val(self.m_operatorScannedCB, opl)

        return answ


    def _get_current_expr(self, pf : PictureSelectionFilter):
        answ = None
        if is_strict(pf.kennung):
            answ = Picture.ReadableId == pf.kennung
            return answ
        elif is_def(pf.kennung):
            answ = sqp.IsLike(Picture.ReadableId, pf.kennung.replace("*", "%"))

        if is_strict(pf.title):
            answ = self._add2exp(answ, Picture.Title==pf.title)
        elif is_def(pf.title):
            answ = self._add2exp(answ, sqp.IsLike(Picture.Title, pf.title.replace("*", "%")))

        if pf.datetaken is not None:
            if pf.datetakenop == "=":
                answ = self._add2exp(answ, Picture.TakenDate == pf.datetaken)
            elif pf.datetakenop == ">":
                answ = self._add2exp(answ, Picture.TakenDate > pf.datetaken)
            elif pf.datetakenop == "<":
                answ = self._add2exp(answ, Picture.TakenDate < pf.datetaken)

        if pf.datescanned is not None:
            if pf.datescannedop == "=":
                answ = self._add2exp(answ, Picture.ScanDate == pf.datescanned)
            elif pf.datescannedop == ">":
                answ = self._add2exp(answ, Picture.ScanDate > pf.datescanned)
            elif pf.datescannedop == "<":
                answ = self._add2exp(answ, Picture.ScanDate < pf.datescanned)


        return answ
    
    def _fill_dialog(self):
        #find all those pictures that have not been connected to the current person
        f = self._get_current_filter()
        exp = self._get_current_expr(f)
        q = sqp.SQQuery(self._fact, Picture).where(exp).order_by(sqp.OrderInfo(Picture.Created, sqp.OrderDirection.DESCENDING))

        ct = 0
        self._picdata = []
        self.m_picturesLCTRL.DeleteAllItems()
        for ppi in q:
            if ct >= 100:
                break
            
            self._picdata.append(ppi)

            idx = self.m_picturesLCTRL.InsertItem(self.m_picturesLCTRL.GetColumnCount(), ppi.readableid)
            self.m_picturesLCTRL.SetItemData(idx, ct)
            self.m_picturesLCTRL.SetItem(idx, 1, ppi.title)
            self.m_picturesLCTRL.SetItem(idx, 2, self._asds(ppi.takendate))
            self.m_picturesLCTRL.SetItem(idx, 3, self._asds(ppi.scandate))
            ct += 1

    def showmodal(self):
        self._init_gui()
        self._fill_dialog()
        res = self.ShowModal()
        if res is wx.ID_CANCEL:
            self._selection = []
            return res
        
        selidx = self.m_picturesLCTRL.GetFirstSelected()
        if selidx == -1:
            return res
        
        while(selidx != -1):
            picpos = self.m_picturesLCTRL.GetItemData(selidx)
            self._selection.append(self._picdata[picpos])
            selidx = self.m_picturesLCTRL.GetNextSelected(selidx)

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