import os
import shutil
import tempfile as tmpf
import datetime
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PictureInfoBit, FluffyMonthCat, DataGroup, GroupTypeCat
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from DocArchiver import DocArchiver
from EditInfoBitDialog import EditInfoBitDialog

class EditPictureDialog(gg.geditPictureDialog):
    
    @property
    def picture(self):
        return self._picture
    
    @property
    def configuration(self):
        return self._configuration
    
    def __init__(self, parent, fact : sqp.SQFactory, picture : Picture):
        super().__init__(parent)
        self._currentpic_extr = None
        self._fact = fact
        self._configuration = parent._configuration
        self._docarchive = parent.docarchive
        self._fluffymonths = self._get_fluffy_months()
        self._pictgroups = self._get_pictgroups()
        tdir = tmpf.gettempdir()
        self.extdir = tdir + os.path.sep + self._configuration.get_value("archivestore", "localtemp")
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"
        self._picture = picture
        self.m_staticBM = None
        self._create_infobit_cols()

    def _get_fluffy_months(self):
        langcode = self._configuration.get_value("gui", "language") 
        return sqp.SQQuery(self._fact, FluffyMonthCat).where(FluffyMonthCat.LangCode==langcode).as_list()
    
    def _get_pictgroups(self):
        return sqp.SQQuery(self._fact, DataGroup).where(DataGroup.GroupType=="PICT").order_by(DataGroup.OrderNum).as_list()
    
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
    
    def _add_ibline(self, dataidx,  ib : PictureInfoBit):
        lct = self.m_zusatzinfoLCT
        idx = lct.InsertItem(lct.GetColumnCount(), self._eds(ib.infodate))
        lct.SetItemData(idx, dataidx)
        lct.SetItem(idx, 1, self._ess(ib.suppliedby))
        lct.SetItem(idx, 2,  self._ess(ib.infocontent))

    def _fill_ibcols(self):
        if self._picture.pictinfobits is None: return

        idx = 0
        for ib in self._picture.pictinfobits:
            self._add_ibline(idx, ib)
            idx += 1

    def pgshow(self, arg):
        return arg.name
    
    def _fill_dialog(self):
        p = self._picture
        self._fact.fill_joins(p, Picture.PictInfoBits, 
                              Picture.PictureGroup)
        GuiHelper.set_val(self.m_kennummerTB, p.readableid)
        GuiHelper.set_sqp_objval(self.m_groupCB, p.picturegroup, self.pgshow, self._pictgroups)
        GuiHelper.set_val(self.m_titelTB, p.title)
        GuiHelper.set_val(self.m_beschreibungTB, p.settledinformation)
        GuiHelper.set_val(self.m_scanDatumDP, p.scandate)
        GuiHelper.set_val(self.m_aufnahmeDatumDP, p.takendate)
        GuiHelper.set_val(self.m_fluffytakenmonthCB, p.fluftakenmonth, self._fluffymonths)
        GuiHelper.set_val(self.m_fluffytakenyearSPCTRL, p.fluftakenyear)
        self._display_document()
        self._fill_ibcols()

    def showmodal(self):
        self._fill_dialog()
        res = self.ShowModal()
        if res is wx.ID_CANCEL:
            return res
        
        p = self._picture
        p.readableid = GuiHelper.get_val(self.m_kennummerTB)
        p.picturegroup = GuiHelper.get_sqp_objval(self.m_groupCB, self._pictgroups)
        if p.picturegroup is not None:
            p.groupid = p.picturegroup._id
        else:
            p.groupid = None
        p.title = GuiHelper.get_val(self.m_titelTB)
        p.settledinformation = GuiHelper.get_val(self.m_beschreibungTB)
        p.scandate = GuiHelper.get_val(self.m_scanDatumDP)
        p.takendate = GuiHelper.get_val(self.m_aufnahmeDatumDP)
        p.fluftakenmonth = GuiHelper.get_val(self.m_fluffytakenmonthCB, self._fluffymonths)
        p.fluftakenyear = GuiHelper.get_val(self.m_fluffytakenyearSPCTRL)

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
            raise Exception("Unbekanntes Bildformat")

        img = self._scaleimagetomax(img, 300, 200)
        bm = img.ConvertToBitmap()
        if self.m_staticBM is not None:
            self.m_bitmapPAN.RemoveChild(self.m_staticBM) #remove any exiting image

        self.m_staticBM = wx.StaticBitmap(self.m_bitmapPAN, bitmap=bm)
        self._currentpic_extr = extr
        
    def uploadPicture(self, event):
        if self._picture.filepath is not None:
            GuiHelper.show_error("Bitte entferne zuerst das bereits angehängte Bild")
            return

        with wx.FileDialog(self, "Dateiauswahl", wildcard="Bitmap Dateien |*.png; *.bmp; *.jpg; *.jpeg| Alle Dateien | *.*",
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

    def viewPicture(self, event):
        if self._currentpic_extr is None:
            return
        try:
            GuiHelper.openbysys(self._currentpic_extr)
        except Exception as exc:
            GuiHelper.show_error("Unbehandelter Fehler beim Versuch das Bild zu öffnen.\nText der Originalmeldung: {}".format(exc))

    def downloadPicture(self, event):
        if self._picture.filepath is None:
            return
        
        dd = wx.DirDialog(self, "Zielpfad auswählen")
        ddres = dd.ShowModal()
        if ddres != wx.ID_OK:
            return
        
        targpath = dd.GetPath()
        fname = self._docarchive.extract_file(self._picture.filepath, targpath)

        GuiHelper.show_message("Die Datei wurde nach {} aus dem Archiv heruntergeladen".format(fname))

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
        
    def addInfoBit(self, event):
        newib = PictureInfoBit(targetid = self._picture._id,
                               infocontent="<Infotext hier>",
                               infodate = datetime.datetime.now())
        self._fact.flush(newib)

        self._picture.pictinfobits.append(newib)
        idx = len(self._picture.pictinfobits)-1
        self._add_ibline(idx, newib)

    def editInfoBit(self, event):
        selib = GuiHelper.get_selected_fromlctrl(self.m_zusatzinfoLCT, self._picture.pictinfobits)
        if selib is None: return

        dial =  EditInfoBitDialog(self, self._fact, selib)
        res = dial.showmodal()

        if res == wx.ID_CANCEL: return

        self.m_zusatzinfoLCT.DeleteAllItems()
        self._fill_ibcols()

    def removeInfoBit(self, event):
        selib = GuiHelper.get_selected_fromlctrl(self.m_zusatzinfoLCT, self._picture.pictinfobits)
        if selib is None: return

        res = wx.MessageBox("Soll die Information wirklich gelöscht werden?", "Rückfrage", style=wx.YES_NO, parent=self)
        if res == wx.YES:
            self._fact.delete(selib)
            
            self.m_zusatzinfoLCT.DeleteAllItems()
            remid = -1
            ct = 0
            for ib in self._picture.pictinfobits:
                if ib._id == selib._id:
                    remid = ct
                ct += 1

            if remid >= 0:
                self._picture.pictinfobits.pop(remid)

            self._fill_ibcols()

        
