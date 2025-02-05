import os 
import datetime as dt
import time
import shutil as shu
import sqlitepersist as sqp
import mylogger as mylo
from backgroundworkers.BgWorker import BgWorker
from backgroundworkers.BgBasics import *

from PersistClasses import Picture, DataGroup

from DocArchiver import DocArchiver

class BgMassArchivingBase(BgWorker):
    
    def __init__(self, notifywin, paras : dict):
        super().__init__(notifywin)
        self.paras = paras
        self._fact = paras["fact"]
        self._files = paras["files"]
        self._logger = paras["logger"]
        self._docarchiver = paras["docarchiver"]
        self._machlabel = paras["machlabel"]

        assert type(self._files) is list
        assert type(self._logger) is mylo.Logger
        assert type(self._fact) is sqp.SQFactory
        assert type(self._docarchiver) is DocArchiver

        self._groups = None
        self._lastid = None

    def _calc_title(self, filepath : str):
        """try to calculate a title from the filename
            first we split the filename at spaces and underscores to get different words, additionally we split the
            words at position where capitalization changes from non capital to capital letters
        """
        pathparts = os.path.split(filepath)
        filename = pathparts[-1]
        (name, ext) = os.path.splitext(filename)
        
        name = name.replace("\t", " ")
        name = name.replace("_", " ")
        parts = name.split() #split at any whitespace

        first = True
        answ = None
        for part in parts:
            if answ is None:
                answ = self._get_subname_parts(part)
            else:
                answ += " " + self._get_subname_parts(part)

        return answ

    def _get_subname_parts(self, txt : str):
        if txt is None: return None
        if len(txt)==0: return txt

        lastupper = True
        answ = ""
        for c in txt:
            if c.isupper(): 
                if not lastupper:
                    answ += " "
                lastupper = True
            else:
                lastupper = False

            answ += c

        lastdigit = txt[0].isdigit()
        answ2 = ""

        for c in answ:
            if c.isdigit(): 
                if not lastdigit:
                    answ2 += " "
                lastdigit = True
            else:
                if lastdigit:
                    answ2 += " "
                lastdigit = False

            answ2 += c

        return answ2
    
    def _calc_group(self, fpath : str, grouptype : str) -> DataGroup:
        """Try to get a group from the parent dir where the file is located
           When we find a group with the same name - thats the group we put the
           picture data in
        """
        #cache groups
        if self._groups is None:
            self._groups = {}
            groups = sqp.SQQuery(self._fact, DataGroup).where(DataGroup.GroupType==grouptype).as_list()

            for group in groups:
                self._groups[group.name] = group

        pathdir = os.path.dirname(fpath)
        abovedirs, pardir = os.path.split(pathdir)

        if pardir in self._groups:
            return self._groups[pardir]
        else:
            return None
        
    def _get_best_scandate(self, fpath):
        timestamp = os.path.getctime(fpath)
        return dt.datetime.fromtimestamp(timestamp)

    def _move_file2done(self, fpath):
        logger = self._logger
        pdir,fname = os.path.split(fpath)
        targdir = os.path.join(pdir, "done")

        if not os.path.exists(targdir): os.mkdir(targdir)

        logger.debug("Moving source file <{}> to donedir <{}>",
                     fpath,
                     targdir)
        
        shu.move(fpath, targdir)
        
    def _create_readid(self):
        """create a new readabel id and try to make sure that it is unique"""
        tsp = dt.datetime.now()
        newid = "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self._machlabel, tsp) 
        if self._lastid is not None and self._lastid == newid:
            time.sleep(0.1) #wait 1/10 of a second that should change the %f part
            tsp = dt.datetime.now()
            newid = "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self._machlabel, tsp) 

        self._lastid = newid
        return newid