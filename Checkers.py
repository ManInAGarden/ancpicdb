import datetime
import sqlitepersist as sqp
from PersistClasses import Picture, Person, FullPerson, Document

class _CheckerBase():
    def __init__(self, factory):
        self._fact = factory

    def do_checks(self):
        raise Exception("Method do_checks must be overriden, this is doChecks in _CheckerBase!")
    
    def is_empty_str(self, val : str) -> bool:
        return val is None or len(val) == 0


class PictureChecker(_CheckerBase):
    
    def _chk_data_consistency(self) -> dict:
        allpics = sqp.SQQuery(self._fact, Picture).where().as_list()
        answ = {"Kennung fehlt":{},
                "Bild ohne Gruppe":{},
                "Titel fehlt" : {},
                "Kein Archiveintrag":{}
                }
        
        for pic in allpics:
            if self.is_empty_str(pic.readableid):
                answ["Kennung fehlt"][pic.__str__()] = pic
            if pic.picturegroup is None:
                answ["Bild ohne Gruppe"][pic.__str__()] = pic
            if self.is_empty_str(pic.title):
                answ["Titel fehlt"][pic.__str__()] = pic
            if self.is_empty_str(pic.filepath):
                answ["Kein Archiveintrag"][pic.__str__()] = pic

        return answ
    
    def do_checks(self) -> dict:
        subansw = self._chk_data_consistency()

        return subansw

class PersonChecker(_CheckerBase):

    def _chk_data_consistency(self) -> dict:
        allpers = sqp.SQQuery(self._fact, FullPerson).where().as_list()
        answ = {"Geschlecht fehlt":{},
                "Lebensdaten fehlen":{},
                "Lebensdaten unvollständig":{},
                "Lebensdaten widersprüchlich" : {},
                "Namensbestandteile":{},
                "Eltern widersprüchlich":{}
                }
        
        for pers in allpers:
            self._fact.fill_joins(pers, 
                                  FullPerson.Father, 
                                  FullPerson.Mother)
            
            if pers.biosex is None:
                answ["Geschlecht fehlt"][pers.as_string()] = pers
            
            if pers.birthdate is not None:
                by = pers.birthdate.year
            elif pers.birthyear is not None:
                by = pers.birthyear
            else:
                by = None

            if pers.deathdate is not None:
                dy = pers.deathdate.year
            elif pers.deathyear is not None:
                dy = pers.deathyear
            else:
                dy = None

            if by == 0: by = None
            if dy == 0: dy = None

            if by is None:
                if dy is None:
                    answ["Lebensdaten fehlen"][pers.as_string()] = pers
                elif dy is not None:
                    answ["Lebensdaten unvollständig"][pers.as_string()] = pers
            else:
                if dy is None:
                    age = datetime.datetime.now().year - by
                    if age > 100:
                        answ["Lebensdaten unvollständig"][pers.as_string()] = pers
                else:
                    age = dy - by
                    if age > 100:
                        answ["Lebensdaten widersprüchlich"][pers.as_string()] = pers
                        

            if self.is_empty_str(pers.firstname):
                answ["Namensbestandteile"][pers.as_string()] = pers
            elif self.is_empty_str(pers.name):
                answ["Namensbestandteile"][pers.as_string()] = pers

            if pers.fatherid is not None and pers.motherid is not None and pers.fatherid == pers.motherid:
                answ["Eltern widersprüchlich"][pers.as_string()] = pers

        return answ
    
    def do_checks(self) -> dict:
        subansw = self._chk_data_consistency()

        return subansw

class DocumentChecker(_CheckerBase):
    pass
