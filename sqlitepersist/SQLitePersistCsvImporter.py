from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *
from .SQLitePersistQueryParts import *

import csv

class SQLitePersistCsvImporter():
    
    def __init__(self, impcls : PBase, fact : SQFactory, itemdelim: str =',', stringdelim : str ='"'):
        self._delimitm = itemdelim
        self._delimstr = stringdelim
        self._fact = fact
        self._impcls = impcls


    def do_import(self, f):
        dr = csv.DictReader(f)
        lc = 0

        for row in dr:
            obj = self._create_instance(self._impcls, row)
            of = self._fact.ForceWrite
            self._fact.ForceWrite = True #tell the fact to try an insert after the update for db-writes failed, this way we can write instert data with existing _ids
            try:
                self._fact.flush(obj)
            finally:
                self._fact.ForceWrite = of #get back to previous forcewrite state
            lc += 1

        return lc



   
    def _create_instance(self, cls : PBase, row):
        """create an instance of the object from date in the row (filled columns)
        """
        inst = cls()
        #inst._dbvaluescache = {} #create a new cache fpr the old values as read from row
        vd = inst._get_my_memberdict()

        jembs = []
        jlists = []
        ilists = []
        for key, value in vd.items():
            #if hasattr(inst, key) and getattr(inst, key) is not None:
            #    continue
            
            decl = value._declaration
            declt = type(decl)
            
            if declt is JoinedEmbeddedObject:
                #if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                #    jembs.append(decl)
                pass #ignore these
            elif declt is JoinedEmbeddedList:
                #if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                #    jlists.append(decl)
                pass
            elif declt is IntersectedList:
                #if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                #    ilists.append(decl)
                pass
            elif declt is Catalog:
                dbdta = row[key]
                if dbdta is not None and len(dbdta)==0:
                    dbdta = None

                cate = self._fact._get_fullcatentry(value, dbdta)
                setattr(inst, key, cate)
                #inst._dbvaluescache[key] = cate
            elif declt is Blob:
                dbdta = row[key]
                self._stmtlogger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, "blobdata..."))
                try:
                    blobby = decl.to_innertype(dbdta)
                    setattr(inst, key, blobby)
                    #inst._dbvaluescache[key] = blobby
                except Exception as ex:
                    #self._stmtlogger.log_dtafill("ERROR: <{0}> contents: <{1}> - Originalmeldung {2}".format(key, dbdta, str(ex)))
                    raise Exception("Unerwarteter Fehler beim Versuch das Feld {0} einer Instanz der Klasse {1} mit <{2}> zu füllen. Originalmeldung: {3}".format(key, decl, "blobdata...", str(ex)))
            else:
                dbdta = row[key]
                if len(dbdta)==0:
                    dbdta = None

                #self._stmtlogger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, dbdta))
                try:
                    inty = decl.to_innertype(dbdta)
                    setattr(inst, key, inty)
                    #inst._dbvaluescache[key] = inty
                except Exception as ex:
                    #self._stmtlogger.log_dtafill("ERROR: <{0}> contents: <{1}> - Originalmeldung {2}".format(key, dbdta, str(ex)))
                    raise Exception("Unerwarteter Fehler beim Versuch das Feld {0} einer Instanz der Klasse {1} mit <{2}> zu füllen. Originalmeldung: {3}".format(key, decl, dbdta, str(ex)))

        return inst
