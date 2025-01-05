from enum import Enum
import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import Document, Picture

class RegisterDialogStyle(Enum):
    UNKNOWN = 0
    DOCUMENT = 1
    PICTURE = 2
    
class RegisterDialog(gg.gRegisterDialog):
    
    
    def __init__(self, parent, fact, docls):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self.style = RegisterDialogStyle.UNKNOWN
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self.logger = parent.logger
        self.cls = docls
        self._maxsamples = 100
        self._do_prep()

    def _do_prep(self):
        self._dblistdefins =  [
                       {"title": "Archiv-Id", "width": 200, "propname":"readableid" },
                       {"title": "Titel", "width": 100, "propname":"title" },
                       {"title": "angelegt", "width": 50, "propname":"created" },
                       {"title": "geändert", "width": 50, "propname":"lastupdate" },
                    ]
        
        if self.cls is Document:
            title = "Dokumente"
            self.style = RegisterDialogStyle.DOCUMENT
        elif self.cls is Picture:
            title = "Bilder"
            self.style = RegisterDialogStyle.PICTURE
        else:
            raise Exception("Unknown cls in RegisterDialog")

        GuiHelper.set_val(self.m_listTitle, title)


    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _getsamples(self):
        q = sqp.SQQuery(self._fact, self.cls, limit=self._maxsamples).order_by(self.cls.ReadableId)
        return q.as_list()

    def _filldialog(self):
        self.elements = self._getsamples()
        GuiHelper.enable_ctrls(False, self.m_abortWritingBU, self.m_startWritingBU)
        GuiHelper.set_columns_forlstctrl(self.m_elementsLCTR, 
                                         self._dblistdefins)
        
        GuiHelper.set_data_for_lstctrl(self.m_elementsLCTR,
                                       self._dblistdefins,
                                       self.elements)

        