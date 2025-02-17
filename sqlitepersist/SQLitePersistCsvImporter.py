from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *
from .SQLitePersistQueryParts import *

import mylogger as mylo

import csv

class SQLitePersistCsvImporter():
    FORBIDDEN_UPD = ["_id", "created"]

    @classmethod
    def get_std_fname(cls, impcls):
        """get the standard class name used for the class given in clstoimp"""
        return impcls.get_collection_name() + ".csv"

    def __init__(self, 
                 impcls : PBase, 
                 fact : SQFactory, 
                 findwith: list = [PBase.Id],
                 itemdelim: str =',', 
                 stringdelim : str ='"',
                 logger : mylo.Logger = None):
        
        self._delimitm = itemdelim
        self._delimstr = stringdelim
        self._fact = fact
        self._logger : mylo.Logger = logger
        self._impcls = impcls
        self._after_data_do = None #method like doafterflush(self, obj : PBase)
        self._before_data_do = None #line after_data but called before the flush to the db is carried out
        self._findwith = findwith
        self._lastimported = None
        if self._findwith is None or len(self._findwith)==0 or (len(self._findwith)==1 and self._findwith[0]==PBase.Id):
            self._findbyid = True
        else:
            self._findbyid = False


    @property
    def after_data_do(self):
        return self._after_data_do
    
    @after_data_do.setter
    def after_data_do(self, val):
        self._after_data_do = val


    @property
    def before_data_do(self):
        return self._before_data_do
    
    @before_data_do.setter
    def before_data_do(self, val):
        self.beforer_data_do = val

    @property
    def findwith(self):
        return self._findwith
    
    @property
    def imported(self):
        return self._lastimported
    
    def _logdebug(self, frm, *args):
        if self._logger is not None:
            self._logger.debug(frm, *args)

    def _logerror(self, frm, *args):
        if self._logger is not None:
            self._logger.error(frm, *args)

    def _loginfo(self, frm, *args):
        if self._logger is not None:
            self._logger.info(frm, *args)

    def do_import(self, f) -> int:
        if self._findbyid:
            return self.do_importby_id(f)
        else:
            return self.do_importby_unikey(f)

        return len(self._lastimported)
        
    def restrict_on(self, parents_ids : list, resfield) -> int:
        """Restrict the children found before to those where an attribute matches one of the parent ids"""
        if self._lastimported is None or len(self._lastimported)==0: return 0 #nothing to do

        imported = []
        for parid in parents_ids:
            conns = SQQuery(self._fact, self._impcls).where(resfield==parid).as_list()
            for conn in conns:
                if not conn._id in self._lastimported:
                    self._fact.delete(conn)
                else:
                    imported.append(conn._id)

        self._lastimported = imported
        return len(imported)
    
    
    def do_importby_id(self, f) -> int:
        dr = csv.DictReader(f)
        imported = []
        self._loginfo("Starting csv-import for class {}", self._impcls.__name__)
        lc = 0
        for row in dr:
            obj = self._create_instance(self._impcls, row)
            imported.append(obj._id)
            of = self._fact.ForceWrite
            self._fact.ForceWrite = True #tell the fact to try an insert after the update for db-writes failed, this way we can insert data with existing _ids
            try:
                if self._before_data_do is not None:
                    self._before_data_do(obj)

                self._fact.flush(obj)
                
                if self._after_data_do is not None:
                    self._after_data_do(obj)

                lc += 1
            except Exception as exc:
                self._logerror("Error trying to create an instance class <{}> from line# <{}>",
                                self._impcls.__name__, 
                                lc)
                raise exc
            finally:
                self._fact.ForceWrite = of #get back to previous forcewrite state
                
            self._logdebug("Succesfully created id <{}> for class <{}> from line# <{}>",
                           str(obj._id), self._impcls.__name__, len(imported))

        self._lastimported = imported
        return len(imported)

    def do_importby_unikey(self, f) -> int:
        imported = []
        dr = csv.DictReader(f)
        for row in dr:
            obj = self._create_instance(self._impcls, row)
            imported.append(obj._id)
            first = True
            exp = None

            for kv in self._findwith:
                val = self._fact.get_contents(obj, kv)
                if first:
                    exp = kv == val
                    first = False
                else:
                    exp = exp & (kv==val)

            foundl = SQQuery(self._fact, self._impcls, 2).where(exp).as_list()
            
            if len(foundl) > 1: #more than one object found in the db - we cannot do that for now
                raise Exception("Data Import did not find just one object with the given key")
            
            if len(foundl) == 0: #we did not find any object with the given key in the db, so we simply write the new one
                self._fact.flush(obj)
            else:
                self._update_existing(foundl[0], obj)

        self._lastimported = imported
        return len(imported)

    def _update_existing(self, targobj, srcobj):
        #to make everything inside the fact work correctly we transfer any member from src to targ
        #and NOT just manipulate src and write it again

        decls = self._impcls.get_clsdict()
        for mname, mdecl in decls.items():
            if not mname in self.FORBIDDEN_UPD:
                val = getattr(srcobj, mname, None)
                setattr(targobj, mname, val)

        self._fact.flush(targobj)
        
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
                #self._stmtlogger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, "blobdata..."))
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
