from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *
from .SQLitePersistQueryParts import *

import csv

class SQLitePersistCsvExporter():
    
    def __init__(self, cls : PBase, f, itemdelim=',', stringdelim='"'):
        """cls: persistent data class to be handled
           f : file to be used as target for export
           itemdelim: delimitier to be used in the csv to create the columns
           stringdelim: delimiter to enclose strings
        """
        self._file = f
        self._cls = cls
        self._delimitm = itemdelim
        self._delimstr = stringdelim

    def do_export(self, iterab) -> int:
        """exporting the queried data (fetched with iterab) by iterating over it and adding the data line by line
        to the initially opened csv file
        returns the number of written data lines (excluding the header line)
        """

        fnames= self._get_fnames()
        self._fieldnames = fnames

        dw = csv.DictWriter(self._file, 
                            delimiter=self._delimitm, 
                            quotechar=self._delimstr, 
                            fieldnames=fnames,
                            lineterminator="\n")
        
        dw.writeheader()
        elemct = 0
        for elem in iterab:
            rdict = self._get_linedict(elem)
            elemct += 1
            dw.writerow(rdict)

        return elemct

    def _get_fnames(self) -> list:
        cls = self._cls

        answ = []
        memd = cls._classdict[cls]
        for key, val in memd.items():
            data = val.get_declaration()
            if data.is_dbstorable():
                answ.append(key)

        return answ
    

    def _get_linedict(self, insta : PBase) -> str:
        cls = self._cls

        answ = {}
        memd = cls._classdict[cls]
        for key, val in memd.items():
            data = val.get_declaration()
            if data.is_dbstorable():
                dt = val._dectype
                answ[key] = self._get_as_csvstr(dt, insta.__getattribute__(key))

        return answ
    
    def _get_as_csvstr(self, dt, elem):
        """transfer the elem to a csv useable string whatever type it is
        """

        if dt==String:
            if elem is None:
               answ = None        
            else:
               answ = elem
        elif dt==Int:
            if elem is None:
                 answ = ""
            else:
                answ = str(elem)
        elif dt==Float:
            if dt is None:
                answ = None
            else:
                answ = str(dt)
        elif dt==DateTime:
            if elem is None:
                answ = None
            else:
                answ = elem.strftime("%m.%d.%Y %H:%M:%S")
        elif dt == Boolean:
            if elem is None:
                answ = None
            else:
                answ = str(elem)
        elif dt==UUid:
            if elem is None:
                answ = None
            else:
                answ = str(elem)
        elif dt == Catalog:
            if elem is None:
                answ = None
            else:
                answ = elem.code
        else:
             raise Exception("Unsupported typ in _get_as_csvstr")
        
        return answ

        