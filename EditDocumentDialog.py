import tempfile as tmpf
import datetime
import wx
import wx.adv
import sqlitepersist as sqp

from PersistClasses import Document, DocumentInfoBit, DocTypeCat
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from EditInfoBitDialog import EditInfoBitDialog

class EditDocumentDialog(gg.geditDocumentDialog):
    
    @property
    def document(self): return self._document

    @property
    def configuration(self): return self._configuration

    def __init__(self, parent, fact : sqp.SQFactory, document : Document):
        super().__init__(parent)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self._document = document
        self._temp = tmpf.gettempdir()
        self._create_infobit_cols()


    def _create_infobit_cols(self):
        self.m_zusatzinfoLCT.InsertColumn(0, 'Datum')
        self.m_zusatzinfoLCT.InsertColumn(1, 'Quelle')
        self.m_zusatzinfoLCT.InsertColumn(2, 'Inhalt', width=300)

    def _eds(self, dt):
        if dt is None:
            return ""
        
        return "{:%d.%m.%Y}".format(dt)
    
    def _ess(self, val):
        if val is None: return ""

        return val.__str__()
    
    def _add_ibline(self, dataidx,  ib : DocumentInfoBit):
        lct = self.m_zusatzinfoLCT
        idx = lct.InsertItem(lct.GetColumnCount(), self._eds(ib.infodate))
        lct.SetItemData(idx, dataidx)
        lct.SetItem(idx, 1, self._ess(ib.suppliedby))
        lct.SetItem(idx, 2,  self._ess(ib.infocontent))

    def _fill_ibcols(self):
        if self._document.docinfobits is None: return

        idx = 0
        for ib in self._document.docinfobits:
            self._add_ibline(idx, ib)
            idx += 1
            
    def _get_all_types(self):
        return sqp.SQQuery(self._fact, DocTypeCat).where(DocTypeCat.Type=="DOC_TYPE").order_by(DocTypeCat.Value).as_list()
        
    def isempty(self, val):
        if val is None:
            return True
        
        if type(val) is str:
            if len(val)==0:
                return True
            
        return False
    
    def _filldialog(self):
        d = self._document
        self._fact.fill_joins(d, Document.DocInfoBits)
        self._doctypelist = self._get_all_types()
        GuiHelper.set_val(self.m_kennummerTB, d.readableid)
        GuiHelper.set_val(self.m_doctypCB, d.type, fullcat=self._doctypelist)
        GuiHelper.set_val(self.m_titelTB, d.title)
        GuiHelper.set_val(self.m_scanDatumDP, d.scandate)
        GuiHelper.set_val(self.m_produktionsDatumDP, d.productiondate)
        GuiHelper.set_val(self.m_archivepathTB, d.filepath)
        GuiHelper.set_val(self.m_docextTB, d.ext)
        self._fill_ibcols()


    def _scaleimagetomax(self, img : wx.Image, width : int, height : int):
        """scale image so that it fits into a box with the given width and height without defomation """
        oriwi = img.GetWidth()
        orihe = img.GetHeight()
        wif = width / oriwi
        hef = height / orihe

        if wif <= hef:
            neww = int(wif * oriwi)
            newh = int(wif * orihe)
        else:
            neww = int(hef * oriwi)
            newh = int(hef * orihe)

        return img.Scale(width=neww, height=newh)

    def showmodal(self):
        self._filldialog()

        res = self.ShowModal()

        if res == wx.ID_CANCEL:
            return res
        
        p = self._document
        p.readableid = GuiHelper.get_val(self.m_kennummerTB)
        p.type = GuiHelper.get_val(self.m_doctypCB, self._doctypelist)
        p.title = GuiHelper.get_val(self.m_titelTB)
        p.scandate = GuiHelper.get_val(self.m_scanDatumDP)
        p.productiondate = GuiHelper.get_val(self.m_produktionsDatumDP)
        #the follwing fields are readonly in the GUI - no update needed
        #p.filepath = GuiHelper.get_val(self.m_wxarchivepathTB)
        #p.ext = GuiHelper.get_val(self.m_docextTB)
        self._fact.flush(p)
        return res
    
    def uploadDocument(self, event):
        if self._document.filepath is not None:
            GuiHelper.show_error("Bitte entferne zuerst das bereits angehängte Dokument")

        with wx.FileDialog(self, "Dateiauswahl", wildcard="PDFs | *.pdf; | Alle Dateien | *.*",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed his mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                archname, extname = self._docarchive.archive_file(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

            self._document.filepath = archname
            self._document.ext = extname
            self._fact.flush(self._document)
            GuiHelper.set_val(self.m_archivepathTB, archname)
            GuiHelper.set_val(self.m_docextTB, extname)
            self.Refresh()


    def removeDocument(self, event):
        res = wx.MessageBox(parent=self,
                      message="Bist du sicher, dass das Dokument entfernt werden soll?",
                      caption="Rückfrage",
                      style=wx.YES_NO)
        if res == wx.ID_NO:
            return
        
        if self._document.filepath is not None and len(self._document.filepath)>0:
            self._docarchive.remove_file(self._document.filepath)
            self._document.filepath = None
            self._document.ext = None
            GuiHelper.set_val(self.m_archivepathTB, None)
            GuiHelper.set_val(self.m_docextTB, None)
            self._fact.flush(self._document) #make sure that database reflects archive state
            self.Refresh()

    def _downloadtotemp(self, pathname):
        try:
            return self._docarchive.extract_file(pathname, self._temp)
        except IOError:
            wx.LogError("Cannot open file '%s'." % pathname)


    def viewDocument(self, event):
        """download the document temporarily and view it with whatever the op-system wants to open it with"""
        if self._document.filepath is None:
            GuiHelper.show_error("Es wurde kein Dokument archiviert.")
            return

        extrpname = self._downloadtotemp(self._document.filepath)
        GuiHelper.openbysys(extrpname)

    def addInfoBit(self, event):
        newib = DocumentInfoBit(targetid = self._document._id,
                               infocontent="<Infotext hier>",
                               infodate = datetime.datetime.now())
        self._fact.flush(newib)

        self._document.docinfobits.append(newib)
        idx = len(self._document.docinfobits)-1
        self._add_ibline(idx, newib)

    def editInfoBit(self, event):
        selib = GuiHelper.get_selected_fromlctrl(self.m_zusatzinfoLCT, self._document.docinfobits)
        if selib is None: return

        dial =  EditInfoBitDialog(self, self._fact, selib)
        res = dial.showmodal()

        if res == wx.ID_CANCEL: return

        self.m_zusatzinfoLCT.DeleteAllItems()
        self._fill_ibcols()

    def removeInfoBit(self, event):
        selib = GuiHelper.get_selected_fromlctrl(self.m_zusatzinfoLCT, self.document.docinfobits)
        if selib is None: return

        res = wx.MessageBox("Soll die Information wirklich gelöscht werden?", "Rückfrage", style=wx.YES_NO, parent=self)
        if res == wx.YES:
            self._fact.delete(selib)
            
            self.m_zusatzinfoLCT.DeleteAllItems()
            remid = -1
            ct = 0
            for ib in self._document.docinfobits:
                if ib._id == selib._id:
                    remid = ct
                ct += 1

            if remid >= 0:
                self._document.docinfobits.pop(remid)

            self._fill_ibcols()