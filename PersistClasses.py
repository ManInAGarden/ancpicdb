import sqlitepersist as sqp
import datetime

class SexCat(sqp.PCatalog):
     _cattype = "BIO_SEX"
     _langsensitive = True

class PicQualityCat(sqp.PCatalog):
     _cattype = "PICT_QUAL"
     _langsensitive = True

class DocTypeCat(sqp.PCatalog):
     _cattype = "DOC_TYPE"
     _langsensitive = False

class GroupTypeCat(sqp.PCatalog):
     _cattype = "GRP_TYPE"
     _langsensitive = True

class FluffyMonthCat(sqp.PCatalog):
     _cattype = "FLUF_MONTH"
     _langsensitive = True

     def _as_number(self):
          months = ["NOMONTH", 
                  "MONTH01",
                  "MONTH02"
                  "MONTH03"
                  "MONTH04"
                  "MONTH05"
                  "MONTH06"
                  "MONTH07"
                  "MONTH08"
                  "MONTH09"
                  "MONTH10"
                  "MONTH11"
                  "MONTH12"]
          
          return months.index(self.code)

class _InfoBit(sqp.PBase):
     TargetId = sqp.UUid()
     InfoContent = sqp.String()
     InfoDate = sqp.DateTime()
     SuppliedBy = sqp.String()

class PersonInfoBit(_InfoBit):
     """class for informations according persons"""
     pass

class PictureInfoBit(_InfoBit):
     """class for informations according pictures"""
     pass

class DocumentInfoBit(_InfoBit):
     pass

class DataGroup(sqp.PBase):
     Name = sqp.String()
     OrderNum = sqp.Int(default=0)
     GroupType = sqp.Catalog(catalogtype=GroupTypeCat)

     def __str__(self):
          return "{}".format(self.name)
     
class Picture(sqp.PBase):
     """class for pictures normally with people on them"""
     ReadableId = sqp.String()
     GroupId = sqp.UUid()
     PictureGroup = sqp.JoinedEmbeddedObject(targettype=DataGroup, localid=GroupId, autofill=True)
     FilePath = sqp.String()
     Ext = sqp.String()
     ScanDate = sqp.DateTime()
     TakenDate = sqp.DateTime()
     FlufTakenMonth = sqp.Catalog(catalogtype=FluffyMonthCat)
     FlufTakenYear = sqp.Int()
     Title = sqp.String(default="<Titel>")
     SettledInformation = sqp.String()
     Quality = sqp.Catalog(catalogtype=PicQualityCat)
     PictInfoBits = sqp.JoinedEmbeddedList(targettype=PictureInfoBit, foreignid=PictureInfoBit.TargetId, cascadedelete=True)
 
     def __str__(self):
          return "[{}] /{}/ {} {}".format(self.readableid, 
                                      ewn(self.picturegroup),
                                      ewn(self.title), 
                                      ewn(self.takendate))
class Document(sqp.PBase):
     ReadableId = sqp.String()
     GroupId = sqp.UUid()
     Title = sqp.String(default="<Titel>")
     FilePath = sqp.String()
     Ext = sqp.String()
     ScanDate = sqp.DateTime()
     Type = sqp.Catalog(catalogtype=DocTypeCat)
     ProductionDate = sqp.DateTime()
     DocInfoBits = sqp.JoinedEmbeddedList(targettype=DocumentInfoBit, foreignid=DocumentInfoBit.TargetId, cascadedelete=True)

     def __str__(self):
          return "[{}] {} {} {}".format(self.readableid, 
                                      ewn(self.type), 
                                      ewn(self.productiondate),
                                      ewn(self.title))
     
class PersonDocumentInter(sqp.PBase):
     """intersection of Person and Documents"""
     DocumentId = sqp.UUid(uniquegrp="persdocunique")
     PersonId = sqp.UUid(uniquegrp="persdocunique")
     Document = sqp.JoinedEmbeddedObject(targettype=Document, localid="documentid", autofill=True)

     def __str__(self):
          doc = self.document
          return "[{}] {} {} {}".format(doc.readableid, 
                                      ewn(doc.type), 
                                      ewn(doc.productiondate),
                                      ewn(doc.title))

class PersonPictureInter(sqp.PBase):
     PictureId = sqp.UUid(uniquegrp="perspicunique")
     PersonId = sqp.UUid(uniquegrp="perspicunique")
     Picture = sqp.JoinedEmbeddedObject(targettype=Picture, localid="pictureid", autofill=True)
     Subtitle = sqp.String()
     Position = sqp.Int(default=0)

     def __str__(self):
          if self.position is None or self.position==0:
               return "x. [{}] {}".format(self.picture.readableid, self.picture.title)
          else:
               return "{}. [{}] {}".format(self.position, self.picture.readableid, self.subtitle)
class Person(sqp.PBase):
     Name = sqp.String()
     FirstName = sqp.String()
     Rufname = sqp.String()
     BioSex = sqp.Catalog(catalogtype=SexCat)
     NameOfBirth = sqp.String()
     Birthdate = sqp.DateTime()
     BirthYear = sqp.Int()
     BirthMonth = sqp.Catalog(catalogtype=FluffyMonthCat)
     DeathDate = sqp.DateTime()
     DeathMonth = sqp.Catalog(catalogtype=FluffyMonthCat)
     DeathYear = sqp.Int()
     FatherId = sqp.UUid()
     MotherId = sqp.UUid()
     Infotext = sqp.String()
     InfoBits = sqp.JoinedEmbeddedList(targettype=PersonInfoBit, foreignid=PersonInfoBit.TargetId, cascadedelete=True)
     Documents = sqp.IntersectedList(targettype=PersonDocumentInter, interupid="personId", interdownid="documentid")
     Pictures = sqp.IntersectedList(targettype=PersonPictureInter, interupid="personid", interdownid="pictureid")

     def __str__(self):
          answ = "{0} {1}".format(self.firstname, self.name)

          if self.rufname is not None:
               answ += " ({})".format(self.rufname)

          if self.birthdate is not None:
               answ += ": *{:%d.%m.%Y}".format(self.birthdate)
          elif self.birthyear is not None and self.birthyear > 0:
               answ += ": *{}".format(self.birthyear)
          
          if self.deathdate is not None:
               answ += ", +{:%d.%m.%Y}".format(self.deathdate)
          elif self.deathyear is not None and self.deathyear > 0:
               answ += ", +{}".format(self.deathyear)
          
          return answ
     
     def as_string(self):
          """The difference to __str__() is that last name and first name are mixed and the name of birth is given.
               That leads to a more official dispay of the names
          """
          answ = "{}, {}".format(self.name, self.firstname)

          if self.nameofbirth is not None:
               answ += " geb. {}".format(self.nameofbirth)

          if self.birthdate is not None:
               answ += ": *{:%d.%m.%Y}".format(self.birthdate)
          elif self.birthyear is not None and self.birthyear > 0:
               answ += ": *{}".format(self.birthyear)
          
          if self.deathdate is not None:
               answ += ", +{:%d.%m.%Y}".format(self.deathdate)
          elif self.deathyear is not None and self.deathyear > 0:
               answ += ", +{}".format(self.deathyear)
          
          return answ
     
    

class FullPerson(Person):
     _collectionname = "Person" #do not use a separate table for this class. It's only 
     #another version of the person
     
     Father = sqp.JoinedEmbeddedObject(targettype=Person, localid = Person.FatherId)
     Mother = sqp.JoinedEmbeddedObject(targettype=Person, localid = Person.MotherId)
     ChildrenAsFather = sqp.JoinedEmbeddedList(targettype=Person, foreignid=Person.FatherId)
     ChildrenAsMother = sqp.JoinedEmbeddedList(targettype=Person, foreignid=Person.MotherId)     

     
def ewn(val):
     if val is None:
          return ""
          
     if type(val) is str:
          return val
     elif type(val) is datetime.datetime:
          return "{:%d.%m.%Y}".format(val)
     elif type(val) is int:
          return "{}".format(val)
     elif issubclass(type(val), sqp.PCatalog):
          return "{}".format(val.value)
     elif issubclass(type(val), sqp.PBase):
          return val.__str__()
     else:
          raise Exception("Unbekannter Datentyp in PersistClasses.py ewn()")
         