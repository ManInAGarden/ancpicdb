import tempfile as tmpf
import os, subprocess, platform
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
        self._temp = tmpf.gettempdir()

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
        GuiHelper.set_val(self.m_archivepathTB, d.filepath)
        GuiHelper.set_val(self.m_docextTB, d.ext)

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

        with wx.FileDialog(self, "Dateiauswahl", wildcard="Archivierte Dokument Dateien (PDF) |*.pdf | Alle Dateien | *.*",
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

    def _openbysys(self, filepath):
        """let the operating system open a file"""
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))

    def viewDocument(self, event):
        """download the document temporarily and view it with whatever the op-system wants to open it with"""
        if self._document.filepath is None:
            GuiHelper.show_error("Es wurde kein Dokument archiviert.")
            return

        extrpname = self._downloadtotemp(self._document.filepath)
        self._openbysys(extrpname)
