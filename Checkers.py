import sqlitepersist as sqp
from PersistClasses import Picture, Person, Document

class _CheckerBase():
    def __init__(self, factory):
        self._fact = factory

    def do_checks(self):
        raise Exception("Method do_checks must be overriden, this is doChecks in _CheckerBase!")


class PictureChecker(_CheckerBase):
    
    def _chk_data_consistency(self):
        allpics = sqp.SQQuery(self._fact, Picture).where().as_list()
        answ = {"Kennung fehlt":{},
                "Bild ohne Gruppe":{},
                "Titel fehlt" : {},
                "Kein Archiveintrag":{}
                }
        
        for pic in allpics:
            if pic.readableid is None or len(pic.readableid)==0:
                answ["Kennung fehlt"].append({pic.__str__():None})
            if pic.picturegroup is None:
                answ["Bild ohne Gruppe"].append({pic.__str__():None})
            if pic.title is None or len(pic.title)==0:
                answ["Titel fehlt"].append({pic.__str__():None})
            if pic.filepath is None or len(pic.filepath)==0:
                answ["Kein Archiveintrag"].append({pic.__str__():None})

        return answ
    
    def do_checks(self) -> dict:
        subansw = self._chk_data_consistency()

        return subansw

class PersonChecker(_CheckerBase):
    pass

class DocumentChecker(_CheckerBase):
    pass
