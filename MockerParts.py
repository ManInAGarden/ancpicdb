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

    def intersect_persnpic(self, person : Person, pict : Picture, subtitle : str = None, position : int = 0, key : str="") -> PersonPictureInter:
        if not type(person) is Person: raise Exception("intersects first argument must of type Person!")
        if not type(pict) is Picture: raise Exception("intersects first argument must of type Person!")
        
        if pict._id is None: raise Exception("Flush picture before intersecting it to a person")
        if person._id is None: raise Exception("Flush person before intersecting it to a picture")

        if subtitle is not None:
            subt = key + subtitle
        else:
            subt = None

        inter = PersonPictureInter(pictureid=pict._id,
                                   personid=person._id,
                                   position=position,
                                   subtitle=subt)
        self._sqpf.flush(inter)

        return inter

    
    def create_picture_from_dict(self, pictd : dict, key:str = "") -> Person:
        p = Picture()
        
        for dkey, value in pictd.items():
            if dkey=="title" or dkey=="subtitle":
                setattr(p, dkey, key + value)
            else:
                setattr(p, dkey, value)

        self._sqpf.flush(p)
        return p
    
    def create_person_from_dict(self, persd : dict, key:str = "") -> Person:
        p = Person()
        bday = None
        bmonth = None
        byear = None
        for dkey, value in persd.items():
            if dkey=="firstname" or dkey=="name":
                setattr(p, dkey, key + value)
            elif dkey=="birthday":
                bday = value
            elif dkey=="birthmonth":
                bmonth = value
            elif dkey=="birthyear":
                byear = value
            elif dkey=="biosex":
                catval = self._sqpf.getcat(SexCat, value)
                setattr(p, dkey, catval)
            else:
                setattr(p, dkey, value)

        if bday is not None and byear is not None and bmonth is not None:
            p.birthday = datetime.datetime(byear, bmonth, bday)
            bd = None
            bm = None
            by = None
        else:
            bday = None
            p.birthmonth = bmonth
            p.birthyear = byear

        self._sqpf.flush(p)

        return p
            

    def create_pictures(self, data : list, key:str = "") -> list:
        """create pictures from a list of dictionaries, each defining a person
           if not empty all titles will be preceded by the key
        """
        pictures = []
        for picd in data:
            p = self.create_picture_from_dict(picd, key)
            pictures.append(p)

        return pictures


    def create_persons(self, data : list, key:str = "") -> list:
        """create persons from a list of dictionaries, each defining a person
           if not empty all names will be preceded by the key
        """
        persons = []
        for persd in data:
            p = self.create_person_from_dict(persd, key)
            persons.append(p)

        return persons
            

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

        
       

    
