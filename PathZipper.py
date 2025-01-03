import zipfile as zf
import logging
import os
import pathlib as pl

class PathZipper():

    @property
    def srcpath(self):
        return self._srcpath
    
    @property
    def targpath(self):
        return self._targpath
    
    @property
    def fullpath(self):
        return self._targpath + os.sep  + self._filename
    
    def __init__(self, srcpath : str, targpath : str, filename : str, logger = None):
        self._srcpath = srcpath
        self._targpath = targpath
        self._filename = filename
        self._logger = logger

    def _zipdir(self, ziph):
        path = self._srcpath
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))
    def dozip(self):
        """do the zipping work"""
        if not self._logger is None:
            self._logger.info("Doing path backup for path <%s> to zip file <%s>", 
                              self.srcpath,
                              self.fullpath)
        
        with zf.ZipFile(self.fullpath, 'w', zf.ZIP_DEFLATED) as zipf:
            self._zipdir(zipf)

        if not self._logger is None:
            self._logger.info("Succesfully created backupzip %s", self.fullpath)
        