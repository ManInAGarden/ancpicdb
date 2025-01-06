from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *
from .SQLitePersistQueryParts import *

class SQLitePersistCsvImporter():
    
    def __init__(self, impcls : PBase, fact : SQFactory, itemdelim: str =',', stringdelim : str ='"'):
        self._delimitm = itemdelim
        self._delimstr = stringdelim
        self._fact = fact
        self._impcls = impcls

    def _get_header(self, f) -> list:
        headline = f.readline()
        if headline is None or len(headline)==0: raise Exception("CSV must start with a header line")

        cols = headline.split(self._delimitm)

        if len(cols) == 0: raise Exception("CSV header must contain column names separated by the item delimiter")

        self._colinfo = []
        for col in cols:
            self._colinfo.append(col.strip().lower())

        self._csize = len(self._colinfo)


    def _get_parts(self, line):
        instr = False
        currcol = ""
        answ = []
        needcontent = False
        for c in line:
            if c==self._delimstr:
                if instr:
                    instr = False
                else:
                    instr = True
            elif c==self._delimitm:
                if instr:
                   currcol += c 
                else:
                    needone = True
                    if len(currcol)==0:
                        currcol = None
                    answ.append(currcol)
                    currcol = ""
            elif c==' ':
                needone = False
                if instr:
                    currcol += c
            elif c=='\n':
                if instr:
                    currcol += c
            else:
                currcol += c

        if len(currcol) > 0:
            answ.append(currcol)
        elif needone:
            answ.append(None)
        

        return answ

    def do_import(self, f):
        """Do the import of data from a csv file/stream already opened in f
        f : an already opened and positioned csv-stream ready to be read sequentially"""
        self._get_header(f)

        #after consuming the header we read the rest of the file line by line now and create
        #a database entry for every line we can split to columns
        lc = 1 #we already read the 1st line (#0), so we start with 1 here
        for line in f:
            cols = self._get_parts(line)
            
            if len(cols) != self._csize: raise Exception("Anzahl der Spalten in Zeile {} stimmt nicht mit der Titelzeile überein".format(lc))

            obj = self._create_instance(self._impcls, cols)
            self._fact.flush(obj)
            lc += 1


    def _getfromrow(self, key, row):
        idx = self._colinfo.index(key)
        return row[idx]
    
    def _create_instance(self, cls : PBase, row):
        """create an instance of the object from date in the row (filled columns)
        """
        inst = cls()
        inst._dbvaluescache = {} #create a new cache fpr the old values as read from row
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
                if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                    jembs.append(decl)
            elif declt is JoinedEmbeddedList:
                if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                    jlists.append(decl)
            elif declt is IntersectedList:
                if (not hasattr(inst, key) or getattr(inst, key) is None) and decl.get_autofill():
                    ilists.append(decl)
            elif declt is Catalog:
                dbdta = self._getfromrow(key, row)
                cate = self._fact._get_fullcatentry(value, dbdta)
                setattr(inst, key, cate)
                inst._dbvaluescache[key] = cate
            elif declt is Blob:
                dbdta = row[key]
                self._stmtlogger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, "blobdata..."))
                try:
                    blobby = decl.to_innertype(dbdta)
                    setattr(inst, key, blobby)
                    inst._dbvaluescache[key] = blobby
                except Exception as ex:
                    #self._stmtlogger.log_dtafill("ERROR: <{0}> contents: <{1}> - Originalmeldung {2}".format(key, dbdta, str(ex)))
                    raise Exception("Unerwarteter Fehler beim Versuch das Feld {0} einer Instanz der Klasse {1} mit <{2}> zu füllen. Originalmeldung: {3}".format(key, decl, "blobdata...", str(ex)))
            else:
                dbdta = self._getfromrow(key, row)
                #self._stmtlogger.log_dtafill("DF: field: <{0}> contents: <{1}>".format(key, dbdta))
                try:
                    inty = decl.to_innertype(dbdta)
                    setattr(inst, key, inty)
                    inst._dbvaluescache[key] = inty
                except Exception as ex:
                    #self._stmtlogger.log_dtafill("ERROR: <{0}> contents: <{1}> - Originalmeldung {2}".format(key, dbdta, str(ex)))
                    raise Exception("Unerwarteter Fehler beim Versuch das Feld {0} einer Instanz der Klasse {1} mit <{2}> zu füllen. Originalmeldung: {3}".format(key, decl, dbdta, str(ex)))

        # kept for now because maybe these need to initialised with None
        #for jemb in jembs:
        #    self._fill_embedded_object(inst, jemb)

        #for jlist in jlists:
        #    self._fill_embedded_list(inst, jlist)

        #for ilist in ilists:
        #    self._fill_intersected_list(inst, ilist)

        return inst
