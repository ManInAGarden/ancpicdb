import wx
import wx.adv
from PersistClasses import Document, DocumentInfoBit, DocType
import GeneratedGUI as gg
from GuiHelper import GuiHelper

import sqlitepersist as sqp

class EditDocumentDialog(gg.geditDocumentDialog):
    
    @property
    def document(self): return self._document

    def __init__(self, parent, fact : sqp.SQFactory, document : Document):
        super().__init__(parent)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self._document = document

    def _get_all_types(self):
        return sqp.SQQuery(self._fact, DocType).where(DocType.Type=="DOC_TYPE").order_by(DocType.Value).as_list()
        
    def isempty(self, val):
        if val is None:
            return True
        
        if type(val) is str:
            if len(val)==0:
                return True
            
        return False
    
    def _filldialog(self):
        d = self._document
        self._doctypelist = self._get_all_types()
        GuiHelper.set_val(self.m_kennummerTB, d.readableid)
        GuiHelper.set_val(self.m_doctypCB, d.type, fullcat=self._doctypelist)
        GuiHelper.set_val(self.m_titelTB, d.title)
        GuiHelper.set_val(self.m_scanDatumDP, d.scandate)
        GuiHelper.set_val(self.m_produktionsDatumDP, d.productiondate)
        self._display_document()

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

    def _display_document(self):
        """display the document in the bitmap box in appropriate form"""
        if self.isempty(self._document.ext) or self.isempty(self._document.filepath):
            return
        
        extr = self._docarchive.extract_file(self._document.filepath, self.extdir)
        upperext = self._document.ext.upper()

        if upperext in [".BMP", ".JPG", ".JPEG", ".PNG"]:
            img = wx.Image(extr)
        else:
            raise Exception("Unbekanntes Bildformat")

        img = self._scaleimagetomax(img, 300, 200)
        bm = img.ConvertToBitmap()
        if self.m_staticBM is not None:
            self.m_bitmapPAN.RemoveChild(self.m_staticBM) #remove any exiting image

        self.m_staticBM = wx.StaticBitmap(self.m_bitmapPAN, bitmap=bm)

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
        
        self._fact.flush(p)
        return res