import unittest
import sqlitepersist as sqp
from  PersistClasses import *
import MockerParts as mocking
import json
import logging

class TestBase(unittest.TestCase):

    Spf : sqp.SQFactory = None #the persitence factory
    Mck : mocking.Mocker = None #the Mocker-Factory
    PersTables = [sqp.PCatalog, sqp.CommonInter,
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

    @classmethod
    def setUpClass(cls):
        fact = sqp.SQFactory("AncPicDb", "AncPicDbTest.sqlite")
        fact.lang = "DEU"
        cls.Spf = fact
        lhandler = logging.FileHandler(filename="unittest.log", mode="a")
        logger = logging.Logger("unittstlogger", level="DEBUG")
        logger.addHandler(lhandler)
        fact.set_db_dbglevel(logger, "DATAFILL") # use "STMTS for statements only or NONE for no sqlite-debugging at all"

        for tablec in cls.PersTables:
            cls.Spf.try_createtable(tablec)

        cls.Mck = mocking.Mocker(fact)
        try:
            sqp.SQPSeeder(fact, "./seeds/catalogs.json").create_seeddata()
        except Exception as exc:
            print("Data seeding failed with {0}".format(str(exc)))


    @classmethod
    def tearDownClass(cls):
        q = 9 #breakpoint here to check db-contents before everything gets cleaned up after the test
        for tablec in cls.PersTables:
            cls.Spf.try_droptable(tablec)



