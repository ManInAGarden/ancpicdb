import os
import shutil
import tempfile as tmpf
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from DocArchiver import DocArchiver

class EditPictureDialog(gg.geditPictureDialog):
    
    @property
    def picture(self):
        return self._picture
    
    def __init__(self, parent, fact : sqp.SQFactory, picture : Picture):
        super().__init__(parent)
        self._fact = fact
        self._configuration = parent._configuration
        self._docarchive = parent.docarchive
        tdir = tmpf.gettempdir()
        self.extdir = tdir + os.path.sep + self._configuration.get_value("archivestore", "localtemp")
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"
        self._picture = picture
        self.m_staticBM = None

    def _fill_dialog(self):
        p = self._picture
        GuiHelper.set_val(self.m_kennummerTB, p.readableid)
        GuiHelper.set_val(self.m_titelTB, p.title)
        GuiHelper.set_val(self.m_beschreibungTB, p.settledinformation)
        GuiHelper.set_val(self.m_scanDatumDP, p.scandate)
        GuiHelper.set_val(self.m_aufnahmeDatumDP, p.takendate)
        self._display_document()


    def showmodal(self):
        self._fill_dialog()
        res = self.ShowModal()
        if res is wx.ID_CANCEL:
            return res
        
        p = self._picture
        p.readableid = GuiHelper.get_val(self.m_kennummerTB)
        p.title = GuiHelper.get_val(self.m_titelTB)
        p.settledinformation = GuiHelper.get_val(self.m_beschreibungTB)
        p.scandate = GuiHelper.get_val(self.m_scanDatumDP)
        p.takendate = GuiHelper.get_val(self.m_aufnahmeDatumDP)
        
        return res
    
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

    def isempty(self, val):
        if val is None:
            return True
        
        if type(val) is str:
            if len(val)==0:
                return True
            
        return False
    
    def _display_document(self):
        """display the document in the bitmap box in appropriate form"""
        if self.isempty(self._picture.ext) or self.isempty(self._picture.filepath):
            return
        
        extr = self._docarchive.extract_file(self._picture.filepath, self.extdir)
        upperext = self._picture.ext.upper()

        if upperext in [".BMP", ".JPG", ".JPEG", ".PNG"]:
            img = wx.Image(extr)
        else:
            raise Exception("Unbekanntes Bildvormat")

        img = self._scaleimagetomax(img, 300, 200)
        bm = img.ConvertToBitmap()
        if self.m_staticBM is not None:
            self.m_bitmapPAN.RemoveChild(self.m_staticBM) #remove any exiting image

        self.m_staticBM = wx.StaticBitmap(self.m_bitmapPAN, bitmap=bm)
        
    def uploadDocument(self, event):
        if self._picture.filepath is not None:
            GuiHelper.show_error("Bitte entferne zuerst das bereits angehängte Bild")

        with wx.FileDialog(self, "Dateiauswahl", wildcard="PNG Bilder (*.png)|*.png, Bmp Bitmaps (*.bmp)|*.bmp, JPeg Bilder (*.jpg)|*.jpg",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed his mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                archname, extname = self._docarchive.archive_file(pathname)
                self._picture.filepath = archname
                self._picture.ext = extname
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

        self._display_document()

    def removePicture(self, event):
        res = wx.MessageBox(parent=self,
                      message="Bist du sicher, dass das Bild entfernt werden soll?",
                      caption="Rückfrage",
                      style=wx.YES_NO)
        if res == wx.ID_NO:
            return
        
        if self._picture.filepath is not None and len(self._picture.filepath)>0:
            self._docarchive.remove_file(self._picture.filepath)
            self._picture.filepath = None
            self._picture.ext = None
            self._fact.flush(self._picture) #make sure that database reflects archive state
            self.m_bitmapPAN.RemoveChild(self.m_staticBM)
            self.Refresh()
        