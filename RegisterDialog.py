from enum import Enum
import wx
import wx.adv
import BackgroundWorkers as bgw
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
        self.targetfile = None
        self.doclass = docls
        self._bw = None
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self.logger = parent.logger
        self._maxsamples = 100
        self._do_prep()

        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)

    def _do_prep(self):
        self._dblistdefins =  [
                       {"title": "Archiv-Id", "width": 200, "propname":"readableid" },
                       {"title": "Titel", "width": 100, "propname":"title" },
                       {"title": "angelegt", "width": 50, "propname":"created" },
                       {"title": "geändert", "width": 50, "propname":"lastupdate" },
                    ]
        
        if self.doclass is Document:
            title = "Dokumente"
            self.style = RegisterDialogStyle.DOCUMENT
        elif self.doclass is Picture:
            title = "Bilder"
            self.style = RegisterDialogStyle.PICTURE
        else:
            raise Exception("Unknown cls in RegisterDialog")

        GuiHelper.set_val(self.m_listTitle, title)


    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _getsamples(self):
        q = sqp.SQQuery(self._fact, self.doclass, limit=self._maxsamples).order_by(self.doclass.ReadableId)
        return q.as_list()

    def _filldialog(self):
        self.elements = self._getsamples()
        GuiHelper.enable_ctrls(False, self.m_abortWritingBU, self.m_startWritingBU)
        GuiHelper.set_columns_forlstctrl(self.m_elementsLCTR, 
                                         self._dblistdefins)
        
        GuiHelper.set_data_for_lstctrl(self.m_elementsLCTR,
                                       self._dblistdefins,
                                       self.elements)
        
    def workerfinished(self, event):
        GuiHelper.enable_ctrls(True, self.m_startWritingBU)
        GuiHelper.enable_ctrls(False, self.m_abortWritingBU)

    def notifyperc(self, event):
        perc = event.data
        GuiHelper.set_val(self.m_writingGAUGE, perc)

    def fileSelected(self, event):
        """A file has succesfully been selected"""
        self.targetfile = GuiHelper.get_val(self.m_targetfileNameFP)

        GuiHelper.enable_ctrls(True, self.m_startWritingBU)

    def get_doc_title(self):
        if self.style == RegisterDialogStyle.DOCUMENT:
            return "Register der archivierten Dokumente"
        elif self.style == RegisterDialogStyle.PICTURE:
            return "Register der archivierten Bilder und Fotografien"
        else:
            raise Exception("Unknown style in RegisterDialog.get_doc_title")
        

    def startWriting(self, event):
        paras = {
                    "fact": self._fact,
                    "docls" : self.doclass,
                    "targetfile" : self.targetfile,
                    "title": self.get_doc_title()
                }
        self._bw = bgw.BgRegisterWriter(notifywin=self,paras=paras)
        self._bw.start()

        GuiHelper.enable_ctrls(True, self.m_abortWritingBU)
        GuiHelper.enable_ctrls(False, self.m_startWritingBU)

    def abortWriting(self, event):
        if self._bw is None: return

        self._bw.request_abort()
        