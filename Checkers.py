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
    
class DocumentChecker(_CheckerBase):
     
     def _chk_data_consistency(self):
        answ = {"Kennung fehlt":{},
                "Titel fehlt" : {},
                "Kein Archiveintrag":{}
                }
         
        alldocs = sqp.SQQuery(self._fact, Document).where().as_list()
        for doc in alldocs:
            if self.is_empty_str(doc.readableid):
                answ["Kennung fehlt"][doc.__str__()] = doc
                     
            if self.is_empty_str(doc.title):
                answ["Titel fehlt"][doc.__str__()] = doc

            if self.is_empty_str(doc.filepath):
                answ["Kein Archiveintrag"][doc.__str__()] = doc

        return answ

     def do_checks(self) -> dict:
        subansw = self._chk_data_consistency()

        return subansw

class PersonChecker(_CheckerBase):

    def _chk_parent(self, child : Person, parent : Person) -> bool:
        """check wehter a given parent can be the childs parent accoirding to birthdate and deathdates of both
            returns True when suspicous or impossible
        """
        #Schmutzabweiser
        if parent is None:
            return False
        
        years = 365.25
        months = 30
        MIN_PARENT_AGE = 14*years
        MAX_FATHER_DEAD = 9*months

        if child.birthdate is not None:
            if parent.birthdate is not None:
                if (child.birthdate - parent.birthdate).days < MIN_PARENT_AGE:
                    return True
        
        if child.deathdate is not None:
            if parent.deathdate is not None:
                if child.birthdate is not None:
                    #women can't give birth when they're dead
                    if parent.biosex.code == "FEMALE" and (parent.deathdate < child.birthdate):
                        return True
                    elif parent.biosex.code == "MALE" and (parent.deathdate - child.birthdate).days < MAX_FATHER_DEAD:
                        return True
                    
        if child.birthdate is not None and parent.birthdate is not None and child.deathdate is not None and parent.deathdate is not None:
            return False
        
    
        #we have no sufficient exact birth/deathdates. We try death and birthyears now
        cdy = child.cons_death_year
        cby = child.cons_birth_year
        pdy = parent.cons_death_year
        pby = parent.cons_birth_year

        if cby is not None:
            if pby is not None:
                if (cby - pby)*years < MIN_PARENT_AGE:
                    return True
                
            if pdy is not None:
                if (pdy - cby)*years <= (-1*years):
                    return True
                
        return False


    def _chk_data_consistency(self) -> dict:
        allpers = sqp.SQQuery(self._fact, FullPerson).where().as_list()
        answ = {"Geschlecht fehlt":{},
                "Lebensdaten fehlen":{},
                "Lebensdaten unvollständig":{},
                "Lebensdaten widersprüchlich" : {},
                "Namensbestandteile":{},
                "Eltern widersprüchlich":{},
                "Eltern fehlen":{},
                "Alter der Mutter verdächtig":{},
                "Alter des Vaters verdächtig":{}
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

            
            if pers.fatherid is None and pers.motherid is None:
                answ["Eltern fehlen"][pers.as_string()] = pers
            elif pers.fatherid is not None and pers.motherid is not None and pers.fatherid == pers.motherid:
                answ["Eltern widersprüchlich"][pers.as_string()] = pers

            if self._chk_parent(pers, pers.father):
                answ["Alter des Vaters verdächtig"][pers.as_string()] = pers
            if self._chk_parent(pers, pers.mother):
                answ["Alter der Mutter verdächtig"][pers.as_string()] = pers
            
        return answ
    
    def do_checks(self) -> dict:
        subansw = self._chk_data_consistency()

        return subansw


