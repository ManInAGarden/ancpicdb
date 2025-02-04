import datetime as dtm
import uuid
import sqlitepersist as sqp
from PersistClasses import *
from sqlitepersist.SQLitePersistQueryParts import SQQuery

class Mocker(object):
   
    def __init__(self, fact : sqp.SQFactory) -> None:
        self._sqpf = fact
        self._fdef_cache = None

    def create_seeddata(self, filepath):
        # self._mpf._db.drop_collection(MrMsCat.get_collection_name()) #this drops all of the catalogs becaus they are all in the same collection!
        seeder = sqp.SQPSeeder(self._sqpf, filepath)
        seeder.create_seeddata()

    def _create_ref_dict(self, sq : SQQuery) -> dict:
        answ = {}
        for el in sq:
            answ[el.abbreviation] = el

        return answ
    
    def create_picture(self, title="no title", datetaken = None, scandate = None, yeartaken=None, monthtaken=None):
        pic = Picture(title=title,
                      takendate = datetaken,
                      scandate = scandate,
                      fluftakenmonth=monthtaken,
                      fluftakenyear=yeartaken)

        self._sqpf.flush(pic)

        return pic
    
    def create_person(self, 
                      firstname = "Heinrich", name="Gurkenhobel", nameofbirth=None,
                      birthday=None, birthyear= None, birthmonth=None,
                      biosex_code = None):
        
        if birthday is not None and birthyear is not None and birthmonth is not None:
            bday = datetime.datetime(birthyear, birthmonth, birthday)
            bd = None
            bm = None
            by = None
        else:
            bday = None
            bd = birthday
            bm = birthmonth
            by = birthyear

        pers = Person(firstname = firstname,
                        name = name,
                        nameofbirth = nameofbirth,
                        birthdate=bday,
                        birthyear=by,
                        birthmonth=bm)
        
        if biosex_code is not None:
            bs = self._sqpf.getcat(Person.BioSex.get_catalogtype(), biosex_code)
            pers.biosex = bs

        self._sqpf.flush(pers)
        return pers


    def _get_bool(self, valdict, key,  default=False):
        if key not in valdict:
            return default
        else:
            return valdict[key]

    def _get_int(self, valdict, key, default=0):
        if key not in valdict:
            return default
        else:
            return valdict[key]

    def _get_float(self, valdict, key, default=0.0):
        if key not in valdict:
            return default
        else:
            return valdict[key]

        
       

    
