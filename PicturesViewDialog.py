from datetime import datetime
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PictureInfoBit, PersonPictureInter
import sqlitepersist as sqp
from EditPictureDialog import EditPictureDialog
from PictureFilterDialog import PictureFilterDialog
from ConfigReader import ConfigReader
from GuiHelper import GuiHelper
from DocArchiver import DocArchiver

class FilterData():
    def __init__(self):
        self.kennummer = None
        self.title = None
        self.daytaken = None
        self.monthtaken = None
        self.yeartaken = None
        self.group = None

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
        self._filter = FilterData()
        self.logger = parent.logger
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"

    def showmodal(self):
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        """fill dialog with all the pictures"""
        q = sqp.SQQuery(self._fact, Picture).order_by(sqp.OrderInfo(Picture.ScanDate, sqp.OrderDirection.DESCENDING))
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
        self.m_picturesLB.Select(len(self._pictures) -1)

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

    def removePicture(self, event):
        selpic, selpos = GuiHelper.get_selected_fromlb(self.m_picturesLB,
                                                       self._pictures)
        if selpic is None: return

        res = wx.MessageBox("Soll das Bild wirklich gelöscht werden?", "Rückfrage", 
                            style = wx.YES_NO,
                            parent = self)
        
        if res == wx.YES:
            self._fact.begin_transaction("Starting transaction for picture delete")
            try:
                #delete picture from archive
                if selpic.filepath is not None and len(selpic.filepath)>0:
                    self.docarchive.remove_file(selpic.filepath)

                persinters = sqp.SQQuery(self._fact, PersonPictureInter).where(PersonPictureInter.PictureId==selpic._id).as_list()
                for persinter in persinters:
                    self._fact.delete(persinter)

                pictinfobits = sqp.SQQuery(self._fact, PictureInfoBit).where(PictureInfoBit.TargetId==selpic._id).as_list()
                for pictinfobit in pictinfobits:
                    self._fact.delete(pictinfobit)
                    
                self._fact.delete(selpic)

                self._fact.commit_transaction("commiting database operations for picture delete operation")
                done = True
            except Exception as exc:
                self.logger.error("Es ist ein Fehler aufgetreten, Text der Originalmeldung: {}".format(exc))
                self._fact.rollback_transaction("rolling back because of error")
                done = False

            if done:
                self._pictures.pop(selpos)
                self.m_picturesLB.Delete(selpos)

    def applyFilter(self, event):
        edifiltdial = PictureFilterDialog(self, self._fact, self._filter)

        res = edifiltdial.showmodal()

        if res == wx.ID_CANCEL:
            return
            
        