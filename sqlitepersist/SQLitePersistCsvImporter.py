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
                 strictwith: list = [],
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
        self._strictwith = strictwith
        if self._findwith is None or len(self._findwith)==0 or (len(self._findwith)==1 and self._findwith[0]==PBase.Id):
            self._findbyid = True
        else:
            self._findbyid = False

        if self._strictwith is None or len(self._strictwith)==0:
            self._bestrict = False
        else:
            self._bestrict = True

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
    def strictwith(self):
        return self._strictwith
    
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

    def append_to_crealist(self, creadi : dict, obj : PBase):
        """append a created object to the given dict by using its hex representation of _id as a key
        and dictionary with the data for each element. For the key of the inner dict we use the
        strict fields
        """
        indict = {}
        for fdef in self._strictwith:
            val = self._fact.get_contents(obj, fdef)
            key = fdef.get_fieldname()
            indict[key] = val

        creadi[obj._id.hex] = indict

    def _getsrchsexp(self, creaentry):
        first = True
        for strictdef in self._strictwith:
            fname = strictdef.get_fieldname()
            if first:
                first = False
                exp = strictdef == creaentry[fname]
            else:
                exp = exp &  (strictdef == creaentry[fname])

        return exp

    def do_importby_id(self, f):
        dr = csv.DictReader(f)
        lc = 0
        in_csv_lst = {}
        self._loginfo("Starting csv-import for class {}", self._impcls.__name__)
        for row in dr:
            obj = self._create_instance(self._impcls, row)
            of = self._fact.ForceWrite
            self._fact.ForceWrite = True #tell the fact to try an insert after the update for db-writes failed, this way we can insert data with existing _ids
            try:
                if self._before_data_do is not None:
                    self._before_data_do(obj)
                self._fact.flush(obj)
                if self._bestrict:
                    self.append_to_crealist(in_csv_lst, obj)
                if self._after_data_do is not None:
                    self._after_data_do(obj)
            except Exception as exc:
                self._logerror("Error trying to create an instance class <{}> from line# <{}>",
                                self._impcls.__name__, 
                                lc)
                raise exc
            finally:
                self._fact.ForceWrite = of #get back to previous forcewrite state
                
            lc += 1
            self._logdebug("Succesfully created id <{}> for class <{}> from line# <{}>",
                           str(obj._id), self._impcls.__name__, lc)

        if self._bestrict and len(in_csv_lst) > 0:
            for in_csv_key, in_csv_val in in_csv_lst.items():
                exp = self._getsrchsexp(in_csv_val)
                self._logdebug("Selecting all elements of class {} where stricdefs are the same as in {}",
                               self._impcls.__name__,
                               in_csv_val)
                allelems = SQQuery(self._fact, self._impcls).where(exp).as_list()
                self._logdebug("fetched {} elements for approval by strict on {}",
                               len(allelems),
                               in_csv_val)
                for allelem in allelems:
                    if not allelem._id.hex in in_csv_lst:
                        self._logdebug("{} id not approved as been delivered in csv and therefore deleted", 
                                       allelem._id)
                        self._fact.delete(allelem)
                    else:
                        self._logdebug("{} id approved as beeing delivered by csv and not deleted", 
                                       allelem._id)

        return lc

    def do_importby_unikey(self, f):
        dr = csv.DictReader(f)
        lc = 0
        for row in dr:
            obj = self._create_instance(self._impcls, row)
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

            lc += 1

        return lc

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
