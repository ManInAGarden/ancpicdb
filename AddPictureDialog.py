import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, Picture, PictureToPersonSel
from GuiHelper import GuiHelper
import sqlitepersist as sqp

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

    def _fill_dialog(self):
        #find all those pictures that have not been connected to the current person

        
        q = sqp.SQQuery(self._fact, Picture).order_by(sqp.OrderInfo(Picture.Created, sqp.OrderDirection.DESCENDING))

        ct = 0
        self._picdata = []
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