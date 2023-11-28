import os
import sys
import shutil
import logging
import logging.config
import tempfile as tmpf

import wx
import wx.adv
import GeneratedGUI as gg
from ConfigReader import *
from DocArchiver import *
from PersonEditDialog import PersonEditDialog
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import Person, PersonInfoBit, Picture, PictureInfoBit, Document, DocumentInfoBit, PersonDocumentInter, PersonPictureInter


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
        self._docarchive = DocArchiver(apath) #use neew archive

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
			Picture,
            PictureInfoBit,
            Document,
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

		#if Unit in createds:
		#	self.logger.info("Seeding units")
		#	sdr = sqp.SQPSeeder(self._fact, os.path.join(self._apppath, "PexSeeds/units.json"))
		#	sdr.create_seeddata()

    def init_gui(self):
        """fill the gui for the first time. This includes to fetch all initially needed data from the DB"""

        #hevily used data with only a small number of records
        self._persons = self.get_all_persons()
        self.refresh_dash()

    def refresh_dash(self):
        """do a complete refresh of the main GUI with the list of persons and the dependent list of documnents and oictures"""

        self._persons = self.get_all_persons()
        self.m_personsLB.Clear()
            
        if len(self._persons) > 0:
            ps = []
            for p in self._persons:
                ps.append(p.__str__())
        
            self.m_personsLB.InsertItems(ps, 0)
            self.m_personsLB.SetSelection(wx.NOT_FOUND)
            
        #self.m_personsLB.Refresh()
        

    def get_all_persons(self):
        q = sqp.SQQuery(self._fact, Person).order_by(Person.FirstName)
        answ = list(q)

        return answ
    
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
                ct += 1
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
        pedial = PersonEditDialog(frm, self._fact, newp)
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
        pedial = PersonEditDialog(frm, self._fact, edp)
        res = pedial.showmodal()
        if res != wx.ID_OK:
            return
        edp = pedial.flushnget()

        self.refresh_dash()
        

    def deletePerson(self, event):
        selpos = self.m_personsLB.GetSelection()
        if selpos == wx.NOT_FOUND:
            return
        
        dp = self._persons[selpos]

        if GuiHelper.ask_user(self, "Möchtest du wirklich die Person >>{}<< löschen?".format(dp.__str__())) == wx.ID_YES:
            self._fact.delete(dp)
            self.refresh_dash()
        
        


if __name__ == '__main__':
    app = wx.App()
    frm = AncPicDbMain(None) 
    frm.Show()
    app.MainLoop()