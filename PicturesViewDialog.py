from datetime import datetime
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture
import sqlitepersist as sqp
from EditPictureDialog import EditPictureDialog
from ConfigReader import ConfigReader

class PicturesViewDialog(gg.gPicturesViewDialog):
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive

    def __init__(self, parent, fact):
        super().__init__(parent)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        """fill dialog with all the pictures"""
        q = sqp.SQQuery(self._fact, Picture).order_by(Picture.ScanDate)
        self._pictures = list(q)
        piclstrs = []

        for pic in self._pictures:
            piclstrs.append(pic.__str__())

        self.m_picturesLB.AppendItems(piclstrs)

    def _create_readid(self):
        dt = datetime.now()
        return "{0}.{1:%Y%m%d.%H%M%H.%f}".format(self.machlabel, dt)
    
    def addNewPicture(self, event):
        readid = self._create_readid()
        pic = Picture(readableid=readid)
        self._fact.flush(pic)
        self._pictures.append(pic)
        self.m_picturesLB.Append(pic.__str__())

    def editPicture(self, event):
        selpos = self.m_picturesLB.GetSelection()
        if selpos is wx.NOT_FOUND:
            return
        
        pict = self._pictures[selpos]
        edial = EditPictureDialog(self, self._fact, pict)
        res = edial.showmodal()
        if res == wx.ID_OK:
            self._fact.flush(edial.picture)
            self._pictures[selpos] = edial.picture
            piclstrs = []
            for pic in self._pictures:
                piclstrs.append(pic.__str__())

            self.m_picturesLB.SetItems(piclstrs)
        