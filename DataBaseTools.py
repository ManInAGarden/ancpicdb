import sys
import os
import sqlitepersist as sqp
from PersistClasses import Person, PersonInfoBit, DataGroup, Picture, PictureInfoBit, Document, DocumentInfoBit, PersonPictureInter, PersonDocumentInter

class DataBaseTools():

    def __init__(self, conf, logger, name, filepath):
        self._configuration = conf
        self.logger = logger
        self.name = name
        self.filepath = filepath

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


    def _get_app_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        elif __file__:
            return os.path.dirname(__file__)
        else:
            raise Exception("Unsupported constellation when trying to get application path")
    
    
    def init_db(self):
        self._apppath = self._get_app_path()
        dbfilename = self.filepath
        self.logger.info("Initialising database in db-file %s", dbfilename)
        self.makesuredirexists(dbfilename)
        self._fact = sqp.SQFactory("AncPicDb", dbfilename)
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