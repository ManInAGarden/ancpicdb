import sys
import os
import tempfile as tmpf
import sqlitepersist as sqp
from DocArchiver import *
from ConfigReader import ConfigReader
from PersistClasses import Person, PersonInfoBit, DataGroup, Picture, PictureInfoBit, Document, DocumentInfoBit, PersonPictureInter, PersonDocumentInter

class APDBTools():

    @property
    def extractionpath(self):
        return self._extractionpath
    
    @property
    def docarchive(self):
        return self._docarchive
    
    @property
    def fact(self):
        return self._fact
    
    
    def __init__(self, conf : ConfigReader, logger):
        self._configuration = conf
        self.logger = logger
        self._sourcepath = conf.get_value_interp("backup", "sourcepath")

    @classmethod
    def makesuredirexists(cls, filename):
        """make sure the path for a given filename exists, so that the file maybe created in that place"""
        dname = os.path.dirname(filename)
        if os.path.exists(dname):
            if os.path.isdir(dname):
                return
            else:
                raise Exception("Path {} existst but is no directory".format(dname))

        os.makedirs(dname, exist_ok=True)

    def switch_to_db(self, dblocation : str):
        """switch to the database (sqlite DB and archive) with the given location
            wihcih contains an Archive directory and a database file always called 
            AncPicDb.sqlite
        """

        #database
        dbfilename = os.path.join(dblocation,"AncPicDb.sqlite")
        self.filepath = dbfilename
        self._apppath = self._get_app_path()
        self.logger.info("Switching to database in db-file %s", dbfilename)
        self._fact = sqp.SQFactory(name, dbfilename)
        self._fact.lang = "DEU"
        doinits = self._configuration.get_value("database", "tryinits")
        self._fact.set_db_dbglevel(self.logger,
            self._configuration.get_value("database", "dbglevel"))
		
        if doinits:
            self._initandseeddb()

        #Archive
        apath = os.path.join(dblocation, "Archive")
        tdir = tmpf.gettempdir()
        extdir = tdir + os.path.sep + self._configuration.get_value("archivestore", "localtemp")
        if not os.path.exists(extdir):
            os.mkdir(extdir)

        self._extractionpath = extdir
        self.logger.info("Initialising archive temporary path %s", extdir)

        self._archpath = apath
        self.logger.info("Initialising archive path %s", apath)
        if os.path.exists(apath):
            self._docarchive = DocArchiver(apath) #use existing archive
            return self._fact, self._docarchive

        self.logger.info("Archive is empty - initialising archive store")
        dnum = self._configuration.get_value("archivestore", "dirnum")
        if dnum <= 0:
            raise Exception("Configuration Error - dirnum must be a positive integer")
		
        #we are starting for the first time, so we initialize the document archive here
        DocArchiver.prepare_archive(apath, dnum)
        self._docarchive = DocArchiver(apath) #use new archive

        return self._fact, self._docarchive
    



    def _get_app_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        elif __file__:
            return os.path.dirname(__file__)
        else:
            raise Exception("Unsupported constellation when trying to get application path")
    
    
    def init_db(self, name, dbfilename):
        self.filepath = dbfilename
        self._apppath = self._get_app_path()
        self.logger.info("Initialising database in db-file %s", dbfilename)
        self.makesuredirexists(dbfilename)
        self._fact = sqp.SQFactory(name, dbfilename)
        self._fact.lang = "DEU"
        doinits = self._configuration.get_value("database", "tryinits")
        self._fact.set_db_dbglevel(self.logger,
            self._configuration.get_value("database", "dbglevel"))
		
        if doinits:
            self._initandseeddb()

        return self._fact
    

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


    def init_archive(self, apath):
        tdir = tmpf.gettempdir()
        extdir = tdir + os.path.sep + self._configuration.get_value("archivestore", "localtemp")
        if not os.path.exists(extdir):
            os.mkdir(extdir)

        self._extractionpath = extdir
        self.logger.info("Initialising archive temporary path %s", extdir)

        self._archpath = apath
        self.logger.info("Initialising archive path %s", apath)
        if os.path.exists(apath):
            return DocArchiver(apath) #use existing archive

        self.logger.info("Archive is empty - initialising archive store")
        dnum = self._configuration.get_value("archivestore", "dirnum")
        if dnum <= 0:
            raise Exception("Configuration Error - dirnum must be a positive integer")
		
        #we are starting for the first time, so we initialize the document archive here
        DocArchiver.prepare_archive(apath, dnum)
        self._docarchive = DocArchiver(apath) #use new archive

        return self._docarchive