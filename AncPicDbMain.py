import os
import sys
import shutil
import tempfile as tmpf
import platform

import wx
import wx.adv
import GeneratedGUI as gg
from ConfigReader import *
from DocArchiver import *
from PersonEditDialog import PersonEditDialog
from PicturesViewDialog import PicturesViewDialog
from DocumentsViewDialog import DocumentsViewDialog
from EditPictureDialog import EditPictureDialog
from AddPictureDialog import AddPictureDialog
from AddDocumentDialog import AddDocumentDialog
from EditDocumentDialog import EditDocumentDialog
from GroupsViewDialog import GroupsViewDialog
from DataCheckerDialog import DataCheckerDialog
from ArchiveExtractDialog import ArchiveExtractDialog
from ChangeDbDialog import ChangeDbDialog
from AboutDialog import AboutDialog
from NewDbDialog import NewDbDialog
from GuiHelper import GuiHelper
from PathZipper import PathZipper
from ExportDataDialog import ExportDataDialog, CsvExportSettings
from ABDBTools import APDBTools
from RegisterDialog import RegisterDialog
from WantedPosterPrintDialog import WantedPosterPrintDialog
from ImportCsvDialog import ImportCsvDialog
from CreateBackupDialog import CreateBackupDialog
import sqlitepersist as sqp
import mylogger as mylo
from PersistClasses import Person, PersonInfoBit, DataGroup, Picture, PictureInfoBit, Document, DocumentInfoBit, PersonDocumentInter, PersonPictureInter

MAXPICTITLELEN = 100
MAXDOCTITLELEN = 100

class AncPicDbMain(gg.AncPicDBMain):
    def __init__(self, parent ):
        super().__init__(parent)
        self._version = "1.0.6"
        GuiHelper.set_icon(self)
        self.init_environ()
        self.init_prog()
        self.init_logging()
        self._dbt = APDBTools(self._configuration, self.logger)
        self.init_archive()
        self.init_db()
        self.init_gui()

    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive
    
    @property
    def appdatapath(self):
        """property to get the path where all user modifiable data are located"""
        return self._appdatapath
    
    @property
    def applicationpath(self):
        """return the path wehere the appplication is located
        these files may only be modified by an admin"""
        return self._apppath

    def _get_app_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        elif __file__:
            return os.path.dirname(__file__)
        else:
            raise Exception("Unsupported constellation when trying to get application path")


    def makesuredirexists(self, filename):
        APDBTools.makesuredirexists(filename)


    def expand_dvalue(self, d : dict, name : str) -> dict:
        """expand any value in the dict with the given key recursively
        and return a coopy of the dict"""
        answ = {}
        for key, val in d.items():
            valt = type(val)
            if valt is str:
                if type(key) is str and key==name:
                    newval = os.path.expandvars(val)
                    answ[key] = newval
                else:
                    answ[key] = val
            elif valt is dict:
                answ[key] = self.expand_dvalue(val, name)
            else:
                answ[key] = val

        return answ

    def expand_dvalueO(self, d : dict, name : str):
        """expand any value in the dict with the given key recursively"""
        for key, val in d.items():
            valt = type(val)
            if valt is str:
                if type(key) is str and key==name:
                    newval = os.path.expandvars(val)
                    d[key] = newval #oh oh does this work?!?
            elif valt is dict:
                self.expand_dvalue(val, name)

    def init_environ(self):
        appdtap = os.environ["AppData"]
        self._appdatapath = os.path.join(appdtap, "AncPicDb")
        self.makesuredirexists(os.path.join(self._appdatapath, "dummifile"))

    
    def init_logging(self):
        cdict = self._configuration.get_section("logging")
        confdict = self.expand_dvalue(cdict, "filename")
        
        lvl = confdict.get("level")
        fname = confdict.get("filename")
        rotsize = confdict.get("maxbytes")

        self.logger = mylo.Logger(lvl)
        self.logger.add_handler(mylo.RotatingFileHandler(fname, rotsize))
        self.logger.info("INF Started AncPicDB V{} log level is {}", self._version, lvl)

                        
    def init_prog(self):
        self._apppath = self._get_app_path()
        cnfname = "AncPicDb.conf"

        self._ensure_config(cnfname)
        self._configuration = ConfigReader(os.path.join(self.appdatapath, cnfname))
        self._wantedconfig = WantedPosterPrintDialog.WantedConfig()

        self.storagepath, self.dbname = self._get_storagebasics()

    def _get_last_dir(self, p : str):
        """getting the last dir element of a path"""
        parts = os.path.split(p)
        l = len(parts)
        return parts[l-1]
    
    def _get_all_but_last_dir(self, p : str):
        """getting all but the last dir"""
        parts = os.path.split(p)
        return parts[0]


    def _get_storagebasics(self):
        dbfilename = self._configuration.get_value_interp("database", "filename")
        currdbdir = os.path.dirname(dbfilename)
        storagepath = self._get_all_but_last_dir(currdbdir)
        dbname = self._get_last_dir(currdbdir)
        return storagepath, dbname

    def _ensure_config(self, cnfname):
        """make sure the config exists. if not try to create it from a distributed version
		"""
        tgtcnfpath = os.path.join(self.appdatapath, cnfname)
        if os.path.exists(tgtcnfpath) and os.path.isfile(tgtcnfpath):
            return

        done = False
        #try an already existing conf file in the application path and copy it to the appdata path
        distcnfpath = os.path.join(self.applicationpath, cnfname)
        done = self.trycopycnf(distcnfpath, tgtcnfpath)

        if done:
            return
        
		#try windows default from the application path
        distcnfpath = os.path.join(self._apppath, "AncPicDb######.conf")
        osname = platform.system()
        done = self.trycopycnf(distcnfpath.replace("######", osname), tgtcnfpath)

        if not done:
            raise Exception("No configuration was found and also could not be created from the os-specific configs")

        return    
    
    def trycopycnf(self, src, tgt):
        if os.path.exists(src) and os.path.isfile(src):
            shutil.copy(src, tgt)
            return True
        else:
            return False
        
    def init_archive(self):
        """Initialise the archive at the configured path"""
        apath = self._configuration.get_value_interp("archivestore","path")
        self._docarchive = self._dbt.init_archive(apath)
        self.logger.info("Initialised archive at {}", apath)
        self._wantedconfig._archiver = self._docarchive


    def init_db(self):
        dbfilename = self._configuration.get_value_interp("database", "filename")
        self._fact = self._dbt.init_db("AncPicDb", dbfilename)
        self.logger.info("Initialised DB with database file {}", dbfilename)
        

    def init_gui(self):
        """fill the gui for the first time. This includes to fetch all initially needed data from the DB"""
        
        #heavily used data with only a small number of records
        self.logger.debug("Initialising the GUI starting")
        self._persons = self.get_all_persons()
        self.m_mainWindowSB.SetStatusText("DB: {0}".format(self.dbname), 0)
        
        self._csvexpsettings = None
        
        self.refresh_dash()
        self.logger.debug("Initialising the GUI done")


    def refresh_pic_stat(self):
        """cont the currently available pictures and show result in status bar"""
        allpics = sqp.SQQuery(self._fact, Picture).as_list()
        self.m_mainWindowSB.SetStatusText("Bilder: {0}".format(len(allpics)), 2)

    def refresh_doc_stat(self):
        """count all documents and show result in status bar"""
        alldocs = sqp.SQQuery(self._fact, Document).as_list()
        self.m_mainWindowSB.SetStatusText("Dokumente: {0}".format(len(alldocs)), 3)

    def refresh_dash(self, prevsel : Person = None):
        """do a complete refresh of the main GUI with the list of persons and the dependent list of documnents and oictures"""
        
        self.logger.debug("Refreshing the dash")
        self._persons = self.get_all_persons()

        self.logger.debug("Found {:d} persons to be displayed in the main list", len(self._persons))
        self.m_personsLB.Clear()
            
        if len(self._persons) > 0:
            ps = []
            ct = 0
            sl = wx.NOT_FOUND
            for p in self._persons:
                ps.append(p.as_string())
                if prevsel is not None and prevsel._id == p._id:
                    sl = ct
                ct += 1
        
            self.m_personsLB.InsertItems(ps, 0)
            self.m_personsLB.SetSelection(sl)
            if sl != wx.NOT_FOUND:
                self.refresh_dash_forp(sl)
            else:
                self.m_picturesLB.Clear()
                self.m_documentsLB.Clear()

        self.m_mainWindowSB.SetStatusText("Personen: {0}".format(len(self._persons)), 1)
        self.refresh_pic_stat()
        self.refresh_doc_stat()
        

    def get_all_persons(self):
        q = sqp.SQQuery(self._fact, Person).order_by(Person.Name, Person.FirstName)
        answ = list(q)

        return answ
    
    def get_selected_ppos(self):
        """get the selected persons position in the self._persons list
        returns wx.NOT_FOUND when nothing was selected or the list is empty"""
        if len(self._persons) == 0:
            return wx.NOT_FOUND
        
        return self.m_personsLB.GetSelection()
        
    def _get_limited_str(self, txt : str, maxl : int) -> str:
        if len(txt) > maxl:
            answ = txt[:maxl-3] + "..."
        else:
            answ = txt

        return answ

    def key_by_date(self, picordoc) -> str:
        """returns a string of the form YYYY.MM.DD to be used fpr alphabetical sorting of the date of an object
            missing dateparts are replaced by ZZZZ or ZZ.
        """

        return picordoc.histkey
    

    def refresh_dash_forp(self, pos):
        """refresh the persons details in case a person was selected or the persons data where updated by another
        callback (picture editing/document editing)"""
        pers = self._persons[pos] #we demand that the person had been refreshed in case links where updated!!!!
          #reread the person from the database and also refresh the pictures and documents for the person
        q = sqp.SQQuery(self._fact, Person).where(Person.Id==pers._id)
        self._persons[pos] = q.first()
        pers = self._persons[pos]

        self._fact.fill_joins(pers, 
                              Person.Pictures,
                              Person.Documents)

        self.m_picturesLB.Clear()
        if len(pers.pictures) > 0:
            picsstrs = []
            pers.pictures.sort(key=self.key_by_date)
            for pic in pers.pictures:
                picstr = self._get_limited_str(pic.__str__(), MAXPICTITLELEN)
                picsstrs.append(picstr)
            self.m_picturesLB.AppendItems(picsstrs)

        self.m_documentsLB.Clear()
        if len(pers.documents) > 0:
            docstrs = []
            pers.documents.sort(key=self.key_by_date)
            for doc in pers.documents:
                docstr = self._get_limited_str(doc.__str__(), MAXPICTITLELEN)
                docstrs.append(docstr)
            self.m_documentsLB.AppendItems(docstrs)


    def cleanup_temp(self):
        expa = self._dbt.extractionpath
        """delete any temporary files from the temp-dir"""
        if not os.path.exists(expa):
            return

        if not os.path.isdir(expa):
            return

        list_of_files = []
        for root, dirs, files in os.walk(expa):
            for filename in files:
                list_of_files.append(os.path.join(root,filename))
        fct = 0
        dct = 0
        for filename in list_of_files:
            if os.path.isfile(filename):
                os.remove(filename)
                fct += 1
            elif os.path.isdir(filename):
                os.rmdir(filename)
                dct += 1
				
        #lastly remove the temp-dir used for temporary extraction
        os.rmdir(expa)
        self.logger.debug("Cleaned temporary {} files in {} directories", fct, dct+1)

	    # Handlers for AncPicDBMainFrame events.
    def quit( self, event ):
        """The user selected the menu item "close AncPicDb" """
        self.logger.info("Quitting AncPicDb")
        self.cleanup_temp()
        self.Close()

    def editNewPerson(self, event):
        newp = Person()
        newp.firstname = "<vorname>"
        newp.name = "<Name>"
        pedial = PersonEditDialog(self, self._fact, newp)
        res = pedial.showmodal()
        if res != wx.ID_OK:
            return
        newp = pedial.flushnget()

        self.refresh_dash()

    def editExistingPerson(self,event):
        selpos = self.m_personsLB.GetSelection()
        if selpos == wx.NOT_FOUND:
            return
        edp = self._persons[selpos]
        pedial = PersonEditDialog(self, self._fact, edp)
        res = pedial.showmodal()
        if res != wx.ID_OK:
            return
        edp = pedial.flushnget()

        self.refresh_dash(edp)
        
        

    def deletePerson(self, event):
        selpos = self.m_personsLB.GetSelection()
        if selpos == wx.NOT_FOUND:
            return
        
        dp = self._persons[selpos]

        if GuiHelper.ask_user(self, "Möchtest du wirklich die Person >>{}<< löschen?".format(dp.__str__())) == wx.ID_YES:
            self._fact.delete(dp)
            self.refresh_dash()

    def personSelected(self, event):
        ppos = self.m_personsLB.GetSelection()
        if ppos is wx.NOT_FOUND:
            return
        
        self.refresh_dash_forp(ppos)

    def openViewPicturesDialog(self, event):
        pwdial = PicturesViewDialog(self, self._fact)
        res = pwdial.showmodal()

        #no refresh ist needed in case no person was selected because only pictures for the person may have changed        
        pos = self.get_selected_ppos()
        self.refresh_pic_stat()
        if pos is not wx.NOT_FOUND:
            self.refresh_dash_forp(pos)


    def openViewDocumentsDialog(self, event):
        dwdial = DocumentsViewDialog(self, self._fact)
        res = dwdial.showmodal()
        #no refresh ist needed in case no person was selected because only pictures for the person may have changed        
        pos = self.get_selected_ppos()
        self.refresh_doc_stat()
        if pos is not wx.NOT_FOUND:
            self.refresh_dash_forp(pos)

    def openViewGroupsDialog(self, event):
        grdial = GroupsViewDialog(self, self._fact, self._configuration)
        res = grdial.showmodal()


    def addPicture(self, event):
        selpers, perspos = GuiHelper.get_selected_fromlb(self.m_personsLB, self._persons)
        if selpers is None:
            return
        
        dial = AddPictureDialog(self, self._fact, selpers)
        res = dial.showmodal()

        if res == wx.ID_OK:
            for pic in dial.selection:
                persinterpic = PersonPictureInter(personid=selpers._id,
                                                  pictureid=pic._id)
                self._fact.flush(persinterpic)
        selpers.pictures = None
        self._fact.fill_joins(selpers, Person.Pictures)

        self.refresh_pic_stat()
        self.refresh_dash_forp(perspos)

    def removeDoumentFromPerson(self, event):
        selpers, perspos = GuiHelper.get_selected_fromlb(self.m_personsLB, self._persons)
        if selpers is None:
            return
        
        seldoc, docpos = GuiHelper.get_selected_fromlb(self.m_documentsLB, selpers.documents)
        if seldoc is None:
            return
        
        self._fact.delete(seldoc)
        selpers.documents = None
        self._fact.fill_joins(selpers, 
                              Person.Documents)
        self.refresh_dash_forp(perspos)

    def removePictureFromPerson(self, event):
        selpers, perspos = GuiHelper.get_selected_fromlb(self.m_personsLB, self._persons)
        if selpers is None:
            return
        
        selpic, picpos = GuiHelper.get_selected_fromlb(self.m_picturesLB, selpers.pictures)
        if selpic is None:
            return
        
        self._fact.delete(selpic)
        selpers.pictures = None
        self._fact.fill_joins(selpers, 
                              Person.Pictures)
        self.refresh_dash_forp(perspos)

    def editPersonsPicture(self, event):
        selpers, perspos = GuiHelper.get_selected_fromlb(self.m_personsLB, self._persons)
        if selpers is None:
            return
        
        selpicinter, picpos = GuiHelper.get_selected_fromlb(self.m_picturesLB, selpers.pictures)
        if selpicinter is None:
            return

        picdial = EditPictureDialog(self, self._fact, selpicinter.picture)
        res = picdial.showmodal()
        if res == wx.ID_CANCEL:
            return
        
        self._fact.flush(picdial.picture)
      
        self.refresh_dash_forp(perspos)

    def addDocument(self, event):
        selpers, perspos = GuiHelper.get_selected_fromlb(self.m_personsLB, self._persons)
        if selpers is None:
            return
        
        dial = AddDocumentDialog(self, self._fact, selpers)
        res = dial.showmodal()

        if res == wx.ID_OK:
            for doc in dial.selection:
                persinterdoc = PersonDocumentInter(personid=selpers._id,
                                                   documentid=doc._id)
                self._fact.flush(persinterdoc)

        self.refresh_doc_stat()
             
        selpers.documents = None
        self._fact.fill_joins(selpers, Person.Documents)
        self.refresh_dash_forp(perspos)

    def editPersonsDocument(self, event):
        selpers, perspos = GuiHelper.get_selected_fromlb(self.m_personsLB, self._persons)
        if selpers is None:
            return
        
        seldocinter, docpos = GuiHelper.get_selected_fromlb(self.m_documentsLB, selpers.documents)
        if seldocinter is None:
            return

        docdial = EditDocumentDialog(self, self._fact, seldocinter.document)
        res = docdial.showmodal()
        if res == wx.ID_CANCEL:
            return
        
        self._fact.flush(docdial.document)
        self.refresh_dash_forp(perspos)

    def backupDb(self, event):
        """presents a backup dialog from where a backup of the db may be startet"""
        creatbadial = CreateBackupDialog(self, self._fact, self.dbname)
        res = creatbadial.showmodal()


    def printWantedPosters(self, event):
        wpdial = WantedPosterPrintDialog(self, self._fact, self._docarchive, self._wantedconfig)

        res = wpdial.showmodal()
        if res == wx.ID_OK:
            self._wantedconfig = wpdial.wpconf

    def doDataCheck(self, event):
        chkdial = DataCheckerDialog(self, self._fact)
        res = chkdial.showmodal()
        self.refresh_dash()

    def extractArchive(self, event):
        exadial = ArchiveExtractDialog(self, self._fact)
        res = exadial.showmodal()

    def createNewDb(self, event):
        newdbdial = NewDbDialog(self, self._fact, self.storagepath, self.dbname)
        res = newdbdial.showmodal()

    def changeDb(self, event):
        dbseldial = ChangeDbDialog(self, self.storagepath, self.dbname)
        res = dbseldial.showmodal()

        if res != wx.ID_OK:
            return
        
        # user selected another database - so now we change the db
        newdb = dbseldial.selected_dblocation
        if newdb is None:
            return
        
        self._fact, self._docarchive = self._dbt.switch_to_db(newdb)
        self.dbname = dbseldial.selected_dbname
        self.init_gui()

    def exportDataToCSV(self, event):
        # if we do not have export data yet we start with empty settings
        if self._csvexpsettings is None:
            self._csvexpsettings = CsvExportSettings()

        expdial = ExportDataDialog(self, self._fact, self._csvexpsettings)

        res = expdial.showmodal()

        self._csvexpsettings = expdial.csvexpsettings

    def printPicRegister(self, event):
        regdial = RegisterDialog(self, self._fact, Picture)
        res = regdial.showmodal()

    def printDocRegister(self, event):
        regdial = RegisterDialog(self, self._fact, Document)
        res = regdial.showmodal()

    def importCsv(self, event):
        impdial = ImportCsvDialog(self, self._fact)
        res = impdial.showmodal()
        self.refresh_dash()

    def showAbout(self, event):
        aboutdial = AboutDialog(self, self._fact, self._version, self.dbname, self.storagepath)
        aboutdial.showmodal()
        

if __name__ == '__main__':
    app = wx.App()
    frm = AncPicDbMain(None)
    frm.Show()
    app.MainLoop()