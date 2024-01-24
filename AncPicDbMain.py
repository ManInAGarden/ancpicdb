import os
import sys
import shutil
import logging
import logging.config
import tempfile as tmpf
import datetime

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
from GuiHelper import GuiHelper
from PathZipper import PathZipper
from WantedPosterPrintDialog import WantedPosterPrintDialog
import sqlitepersist as sqp
from PersistClasses import Person, PersonInfoBit, DataGroup, Picture, PictureInfoBit, Document, DocumentInfoBit, PersonDocumentInter, PersonPictureInter


class AncPicDbMain(gg.AncPicDBMain):
    def __init__(self, parent ):
        super().__init__(parent)
        self._version = "0.9.0"

        self.init_environ()
        self.init_prog()
        self.init_logging()
        self.init_archive()
        self.init_db()
        self.init_gui()

    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive

    def _get_app_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        elif __file__:
            return os.path.dirname(__file__)
        else:
            raise Exception("Unsupported constellation when trying to get application path")

    def makesuredirexists(self, filename):
        """make sure the path for a given filename exists, so that the file maybe created in that place
        """
        dname = os.path.dirname(filename)
        if os.path.exists(dname):
            if os.path.isdir(dname):
                return
            else:
                raise Exception("Path {} existst but is no directory".format(dname))

        os.makedirs(dname, exist_ok=True)


    def expand_dvalue(self, d : dict, name : str):
        """expand any value in the dict with the given key recurseively"""
        for key, val in d.items():
            valt = type(val)
            if valt is str:
                if type(key) is str and key==name:
                    newval = os.path.expandvars(val)
                    d[key] = newval #oh oh does this work?!?
            elif valt is dict:
                self.expand_dvalue(val, name)

    def init_environ(self):
        if sys.platform.startswith("linux"):
            if "APPDATA" not in os.environ:
                appdtap = os.path.expandvars("${HOME}/.AppData")
                self.makesuredirexists(os.path.join(appdtap, "AncPicDb", "dummifile"))
                os.environ["AppData"] = appdtap
        else:
            appdtap = os.environ["AppData"]
            self.makesuredirexists(os.path.join(appdtap, "AncPicDb", "dummifile"))

    
    def init_logging(self):
        cdict = self._configuration.get_section("logging")
        self.expand_dvalue(cdict, "filename")
        logging.config.dictConfig(cdict)
        self.logger = logging.getLogger("mainprog")
        self.logger.info("Started AncPicDB V%s", self._version)
                        
    def init_prog(self):
        self._apppath = self._get_app_path()
        cnfname = "AncPicDb.conf"

        self._ensure_config(cnfname)
        self._configuration = ConfigReader(os.path.join(self._apppath, cnfname))
        self._wantedconfig = WantedPosterPrintDialog.WantedConfig()

    def _ensure_config(self, cnfname):
        """make sure the config exists. if not try to create it from a distributed version
		"""
        tgtcnfpath = os.path.join(self._apppath, cnfname)
        if os.path.exists(tgtcnfpath) and os.path.isfile(tgtcnfpath):
            return

		#try windows
        distcnfpath = os.path.join(self._apppath, "AncPicDb######.conf")
        done = False
        osnames = ["WINDIST", "UBUNTUDIST", "OSXDIST"]
        for osname in osnames:
            done = self.trycopycnf(distcnfpath.replace("######", osname), tgtcnfpath)
            if done:
                break

        if not done:
            raise Exception("No configuration was found and also could not be created from the os-specific configs")
        
    def trycopycnf(self, src, tgt):
        if os.path.exists(src) and os.path.isfile(src):
            shutil.move(src, tgt)
            return True
        else:
            return False
        
    def init_archive(self):
        tdir = tmpf.gettempdir()
        extdir = tdir + path.sep + self._configuration.get_value("archivestore", "localtemp")
        if not path.exists(extdir):
            mkdir(extdir)

        self._extractionpath = extdir
        self.logger.info("Initialising archive temporary path %s", extdir)

        apath = self._configuration.get_value_interp("archivestore","path")
        self.logger.info("Initialising archive path %s", apath)
        if os.path.exists(apath):
            self._docarchive = DocArchiver(apath) #use existing archive
            return

        self.logger.info("Archive is empty - initialising archive store")
        dnum = self._configuration.get_value("archivestore", "dirnum")
        if dnum <= 0:
            raise Exception("Configuration Error - dirnum must be a positive integer")
		
        #we are starting for the first time, so we initialize the document archive here
        DocArchiver.prepare_archive(apath, dnum)
        self._docarchive = DocArchiver(apath) #use new archive
        self._wantedconfig._archiver = self._docarchive

    def init_db(self):
        dbfilename = self._configuration.get_value_interp("database", "filename")
        self.logger.info("Initialising database in db-file %s", dbfilename)
        self.makesuredirexists(dbfilename)
        self._fact = sqp.SQFactory("AncPicDb", dbfilename)
        self._fact.lang = "DEU"
        doinits = self._configuration.get_value("database", "tryinits")
        self._fact.set_db_dbglevel(self.logger,
            self._configuration.get_value("database", "dbglevel"))
		
        if doinits:
            self._initandseeddb()

    def _initandseeddb(self):
        """initalise the db by creating the tables and fill them with seed data"""
        self.logger.info("Creating tables not yet existing and seeding values to tables")
        pclasses = [sqp.PCatalog, sqp.CommonInter,
			Person, 
            PersonInfoBit,
            DataGroup,
			Picture,
            PictureInfoBit,
            Document,
            DocumentInfoBit,
            PersonPictureInter,
            PersonDocumentInter
			]

        createds = []
        for pclass in pclasses:
            done = self._fact.try_createtable(pclass)
            if done:
                createds.append(pclass)

        if sqp.PCatalog in createds:
            self.logger.info("Seeding catalogs")
            sdr = sqp.SQPSeeder(self._fact, os.path.join(self._apppath, "seeds/catalogs.json"))
            sdr.create_seeddata()


    def init_gui(self):
        """fill the gui for the first time. This includes to fetch all initially needed data from the DB"""

        #hevily used data with only a small number of records
        self._persons = self.get_all_persons()

        self.m_mainWindowSB.SetStatusText("DB: {0}".format(self._fact._dbfilename), 0)

        self.refresh_dash()

    def refresh_dash(self, prevsel : Person = None):
        """do a complete refresh of the main GUI with the list of persons and the dependent list of documnents and oictures"""

        self._persons = self.get_all_persons()
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
    
    def get_selected_personandpos(self):
        """get the selected persons position in the self._persons list
        and the person itself as a tuple.
        returns wx.NOT_FOUND, None when nothing was selected or the list is empty"""
        if len(self._persons) == 0:
            return wx.NOT_FOUND, None
        
        pos = self.m_personsLB.GetSelection()
        return pos, self._persons[pos]
    
        
    def refresh_dash_forp(self, pos):
        """refresh the persons details in case a person was selected or the persons data where updated by another
        callback (picture editing/document editing)"""
        pers = self._persons[pos] #we demand that the person had been refreshed in case links where updated!!!!
        self._fact.fill_joins(pers, 
                              Person.Pictures,
                              Person.Documents)

        self.m_picturesLB.Clear()
        if len(pers.pictures) > 0:
            picsstrs = []
            for pic in pers.pictures:
                picsstrs.append(pic.__str__())
            self.m_picturesLB.AppendItems(picsstrs)

        self.m_documentsLB.Clear()
        if len(pers.documents) > 0:
            docstrs = []
            for doc in pers.documents:
                docstrs.append(doc.__str__())
            self.m_documentsLB.AppendItems(docstrs)


    def cleanup_temp(self):
        """delete any temporary files from the temp-dir"""
        if not os.path.exists(self._extractionpath):
            return

        if not os.path.isdir(self._extractionpath):
            return

        list_of_files = []
        for root, dirs, files in os.walk(self._extractionpath):
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
        os.rmdir(self._extractionpath)
        self.logger.info("Cleaned temporary %d files in %d directories", fct, dct+1)

	    # Handlers for AncPicDBMainFrame events.
    def quit( self, event ):
        """The user selected the menu item "close PexDbViewer" """
        self.logger.info("Quitting PexViewer")
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
        if pos is not wx.NOT_FOUND:
            self.refresh_dash_forp(pos)


    def openViewDocumentsDialog(self, event):
        dwdial = DocumentsViewDialog(self, self._fact)
        res = dwdial.showmodal()
        #no refresh ist needed in case no person was selected because only pictures for the person may have changed        
        pos = self.get_selected_ppos()
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
        """creates a backup of the Database and the file archive"""
        dird = wx.DirDialog(self, "Verzeichnis für die Ablage der Sicherung wählen",
                            "",
                            wx.DD_DIR_MUST_EXIST)
        res = dird.ShowModal()
        if res != wx.ID_OK:
            return
        
        targpath = dird.GetPath()
        srcpath = self._configuration.get_value_interp("backup", "sourcepath")
        fname = self._configuration.get_value("backup", "zipname")
        dstr = "{:%Y%m%d}".format(datetime.datetime.now())
        fname = fname.replace("${CreaDate}", dstr)
        pz = PathZipper(srcpath, targpath, fname, self.logger)
        try:
            pz.dozip()
            GuiHelper.show_message("Sicherungskopie unter {} erfolgreich geschrieben.",
                                   pz.fullpath)
        except Exception as exc:
            GuiHelper.show_error("Unbehandelter Fehler in backupdb: {}", exc)

    def printWantedPosters(self, event):
        wpdial = WantedPosterPrintDialog(self, self._fact, self._docarchive, self._wantedconfig)

        res = wpdial.showmodal()
        if res == wx.ID_OK:
            self._wantedconfig = wpdial.wpconf

    def doDataCheck(self, event):
        chkdial = DataCheckerDialog(self, self._fact)
        chkdial.showmodal()


if __name__ == '__main__':
    app = wx.App()
    frm = AncPicDbMain(None) 
    frm.Show()
    app.MainLoop()