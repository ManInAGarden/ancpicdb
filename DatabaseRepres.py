import os
from datetime import datetime

class DatabaseRepres:

    @property
    def name(self):
        return self._name
    
    @property
    def location(self):
        return self._location
    
    @property
    def hasdb(self):
        return self._hasdb
    
    @property
    def hasarchive(self):
        return self._hasarchive
    
    @property
    def created(self):
        return self._created
    

    def __init__(self, name : str, location : str):
        self._name = name
        self._location = location
        self._hasdb = False
        self._hasarchive = False
        self._created = None

        crea = os.path.getctime(location)
        self._created = datetime.fromtimestamp(crea).strftime('%d.%m.%Y %H:%M:%S')
        dbfilepath = os.path.join(location,"AncPicDb.sqlite")
        if os.path.exists(dbfilepath) and os.path.isfile(dbfilepath):
            self._hasdb = True

        archpath = os.path.join(location, "Archive")
        if os.path.exists(archpath) and os.path.isdir(archpath):
            self._hasarchive = True