from sqlitepersist.SQLiteQueryDictGenerator import SQQueryDictGenerator
from .SQLitePersistFactoryParts import *
from .SQLitePersistBasicClasses import *
from .SQLitePersistQueryParts import *

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

        line = self._get_header() + "\n"

        f = self._file
        f.write(line)
        elemct = 0
        for elem in iterab:
            line = self._get_line(elem) + "\n"
            elemct += 1
            f.write(line)

        return elemct

    def _get_header(self) -> str:
        cls = self._cls

        answ = ""
        first = True
        memd = cls._classdict[cls]
        for key, val in memd.items():
            data = val.get_declaration()
            if data.is_dbstorable():
                    if first:
                        answ += key
                        first = False
                    else:
                        answ += self._delimitm + " " + key

        return answ
    

    def _get_line(self, insta : PBase) -> str:
        cls = self._cls

        answ = ""
        first = True
        memd = cls._classdict[cls]
        for key, val in memd.items():
            data = val.get_declaration()
            if data.is_dbstorable():
                    dt = val._dectype
                    if first:
                        answ += self._get_as_csvstr(dt, insta.__getattribute__(key))
                        first = False
                    else:
                        answ += self._delimitm + " " + self._get_as_csvstr(dt, insta.__getattribute__(key))

        return answ
    
    def _get_as_csvstr(self, dt, elem):
        """transfer the elem to a csv useable string whatever type it is
        """

        if dt==String:
            if elem is None:
               answ = self._delimstr + self._delimstr        
            else:
               answ =elem.replace(self._delimstr, "###SD###")
               answ = self._delimstr + answ + self._delimstr        
        elif dt==Int:
            if elem is None:
                 answ = ""
            else:
                answ = str(elem)
        elif dt==Float:
            answ = ""
        elif dt==DateTime:
            if elem is None:
                answ = ""
            else:
                answ = str(elem)
        elif dt == Boolean:
            if elem is None:
                answ = ""
            else:
                answ = str(elem)
        elif dt==UUid:
            if elem is None:
                answ = ""
            else:
                answ = str(elem)
        elif dt == Catalog:
            if elem is None:
                answ = ""
            else:
                answ = elem.code
        else:
             raise Exception("Unsupported typ in _get_as_csvstr")
        
        return answ

        