from datetime import datetime
import csv
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Picture, PictureInfoBit, PersonPictureInter
import sqlitepersist as sqp
from EditPictureDialog import EditPictureDialog
from PictureFilterDialog import PictureFilterDialog
from ConnectedPersonsDialog import ConnectedPersonsDialog
from ConfigReader import ConfigReader
from GuiHelper import GuiHelper
from DocArchiver import DocArchiver
import backgroundworkers as bgw
from FilterData import FilterData
from PictureFilterData import PictureFilterData

class PicturesViewDialog(gg.gPicturesViewDialog):
    """class representing the GUI for viewing pictures in a list control
    """
    PICLISTDEFINS = [
            {"propname" : "readableid", "title": "ID", "width":230},
            {"propname" : "scandate", "title": "Scandatum", "width":100, "format": "{:%d.%m.%Y}"},
            {"propname" : "bestdatestr", "title": "Aufnahmedatum", "width":100},
            {"propname" : "title", "title": "Titel", "width":380},
            #{"propname" : "groupname", "title": "Gruppe", "width":250},
            {"propname" : "picturegroup.groupordername", "title": "Grp#", "width":60}
        ]
    
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive

    def __init__(self, parent, fact):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self._filter = PictureFilterData(fact) #current active filter for the data
        self.logger = parent.logger
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"

        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)

    def workerfinished(self, event : bgw.ResultEvent):
        GuiHelper.enable_ctrls(True, self.m_folderUploadBU)
        self._refilldialog() #refectch pictures from the db and display them in the list

    def notifyperc(self, event):
        perc = event.data
        GuiHelper.set_val(self.m_workingGAUGE, perc)

    def showmodal(self):
        self._filldialog()
        return self.ShowModal()
    
    def _fill_piclist(self):
        GuiHelper.set_data_for_lstctrl(self.m_picturesLCTRL, self.PICLISTDEFINS, self._pictures)

    def _filldialog(self):
        GuiHelper.set_columns_forlstctrl(self.m_picturesLCTRL, self.PICLISTDEFINS)
        self._refilldialog()

    def _get_picdates(self):
        answ = []
        for pic in self._pictures:
            answ.append(str(pic.scandate))

        return answ

    def _refilldialog(self):
        """fill dialog with all the pictures"""
        #requery the picture data
        if self._filter is not None:
            q = self._filter.get_query()
        else:
            q = sqp.SQQuery(self._fact, Picture).order_by(sqp.OrderInfo(Picture.ScanDate, sqp.OrderDirection.DESCENDING))

        self._pictures = q.as_list()
        #picdates = self._get_picdates()
        self._fill_piclist()

    def _create_readid(self):
        dt = datetime.now()
        return "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self.machlabel, dt)
    
    def addNewPicture(self, event):
        readid = self._create_readid()
        pic = Picture(readableid=readid)
        self._fact.flush(pic)

        GuiHelper.append_data_for_lstctrl(self.m_picturesLCTRL, self.PICLISTDEFINS, pic)
        self._pictures.append(pic)
        
        self.m_picturesLCTRL.Select(len(self._pictures) -1)

    def _edictPicture(self, pict):
        edial = EditPictureDialog(self, self._fact, pict)
        res = edial.showmodal()
        if res == wx.ID_OK:
            self._fact.flush(edial.picture)
            self._refilldialog()

    def editPicture(self, event):
        pict = GuiHelper.get_selected_fromlctrl(self.m_picturesLCTRL, self._pictures)
        if pict is None:
            return
        self._edictPicture(pict)
        

    def removePicture(self, event):
        selpics = GuiHelper.get_all_selected_fromlctrl(self.m_picturesLCTRL,
                                                       self._pictures)
        if selpics is None or len(selpics)==0: return

        res = wx.MessageBox("Sollen die selektierten Bilder wirklich gelöscht werden?", "Rückfrage", 
                            style = wx.YES_NO,
                            parent = self)
        
        if res == wx.YES:
            for selpic in selpics:
                self._fact.begin_transaction("Starting transaction for picture delete")
                self.logger.info("Deleting picture {} now,", selpic._id)
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
                    
                    self.logger.debug("Deleted one pictere, {} person/picture intersect(s) and {} picture info bit(s)",
                                      len(persinters), 
                                      len(pictinfobits))
                    
                    self.logger.info("Delete of picture {} succesful", selpic._id)
                except Exception as exc:
                    self.logger.error("An error during picture delete occured. Original message was: {}", exc)
                    self._fact.rollback_transaction("rolling back because of error")

            self._refilldialog()
                

    def applyFilter(self, event):
        edifiltdial = PictureFilterDialog(self, self._fact, self._filter)

        res = edifiltdial.showmodal()

        if res == wx.ID_CANCEL:
            return
            
        self._filter = edifiltdial.filter
        GuiHelper.set_val(self.m_filterInfoTB, self._filter.get_info())
        self._refilldialog()


    def pictureSelected(self, event):
        selpic = GuiHelper.get_selected_fromlctrl(self.m_picturesLCTRL, self._pictures)
        
        GuiHelper.enable_ctrls(selpic != None, 
                                   self.m_downloadPictureBU, 
                                   self.m_editBU,
                                   self.m_deletePictureBU,
                                   self.m_preparePrintBU,
                                   self.m_showConnectedPersonsBU)
        
    def pictureDeselected(self, event):
        selpic = GuiHelper.get_selected_fromlctrl(self.m_picturesLCTRL, self._pictures)
        
        GuiHelper.enable_ctrls(selpic != None, 
                                   self.m_downloadPictureBU, 
                                   self.m_editBU,
                                   self.m_deletePictureBU,
                                   self.m_preparePrintBU,
                                   self.m_showConnectedPersonsBU)
        
        
    def listDblClick(self, event):
        pict = GuiHelper.get_selected_fromlctrl(self.m_picturesLCTRL, self._pictures)
        if pict == None: return
        self._edictPicture(pict)
        
    def doFolderUpload(self, event):
        res = GuiHelper.select_files(self, 
                                     "Bilddateien auswählen",
                                     style=wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

        if res == None:
            return
        
        paras = {}
        paras["fact"] = self._fact
        paras["files"] = res
        paras["logger"] = self.logger
        paras["docarchiver"] = self._docarchive
        paras["machlabel"] = self.machlabel

        self.bg = bgw.BgPictureMassArchiving(notifywin=self, paras = paras)
        self.m_workingGAUGE.Show()

        self.bg.start()

        GuiHelper.enable_ctrls(False, self.m_folderUploadBU)

    def doPreparePrint(self, event):
        """create a list (csv) with info of the selected pictures, ready to be used in a label print
        """
        selpics = GuiHelper.get_all_selected_fromlctrl(self.m_picturesLCTRL, self._pictures)

        if selpics is None or len(selpics)==0: return

        filename = GuiHelper.select_single_file(self, title="Datei für den Export auswählen", 
                                           wildcard="csv-Dateien (*.csv)|*.csv",
                                           style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if filename is None or len(filename)==0: return

        if filename.lower().endswith(".csv"):
            fname = filename
        else:
            fname = filename + ".csv"

        try:
            with open(fname, 'w', newline='', encoding="ansi") as csvfile:
                csvw = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                csvw.writerow(["_id", "readableid", "title", "bestdatestr", "groupname", "grouponum"])
                for sp in selpics:
                    csvw.writerow([sp._id, sp.readableid, sp.title, sp.bestdatestr , sp.groupname, sp.groupordernum])
            
            GuiHelper.show_message("CSV Datei unter <{}> erfolgreich geschrieben", fname)
        except Exception as exc:
            GuiHelper.show_error("Die Datei kann nicht geschrieben werden. {}", exc)

            
    def showConnectedPersons(self, event):
        """display and edit the connections to persons of the selected picture or to the first selected picture if more than
        one picture is selected
        """
        selpic = GuiHelper.get_selected_fromlctrl(self.m_picturesLCTRL, self._pictures)
        
        if selpic is None: return

        conndial = ConnectedPersonsDialog(self, self._fact, selpic)
        conndial.showmodal()
