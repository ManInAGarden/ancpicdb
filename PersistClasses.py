import sqlitepersist as sqp
import datetime

class SexCat(sqp.PCatalog):
     _cattype = "BIO_SEX"
     _langsensitive = True

class DocType(sqp.PCatalog):
     _cattype = "DOC_TYPE"
     _langsensitive = False

class _InfoBit(sqp.PBase):
     TargetId = sqp.UUid()
     InfoContent = sqp.String()

class PersonInfoBit(_InfoBit):
     """class for informations according persons"""
     pass
class PictureInfoBit(_InfoBit):
     """class for informations according pictures"""
     pass

class Picture(sqp.PBase):
     """class for pictures normally with people on them"""
     ReadableId = sqp.String()
     FilePath = sqp.String()
     Ext = sqp.String()
     ScanDate = sqp.DateTime()
     TakenDate = sqp.DateTime()
     Title = sqp.String(default="<Titel>")
     SettledInformation = sqp.String()
     PictInfoBits = sqp.JoinedEmbeddedList(targettype=PictureInfoBit, foreignid=PictureInfoBit.TargetId, cascadedelete=True)
 
     def __str__(self):
          return "[{}] {} {}".format(self.readableid, 
                                      ewn(self.title), 
                                      ewn(self.takendate))
     
class PersonDocumentInter(sqp.PBase):
     """intersection of Person and Documents"""
     DocumentId = sqp.UUid(uniquegrp="persdocunique")
     PersonId = sqp.UUid(uniquegrp="persdocunique")

class PersonPictureInter(sqp.PBase):
     PictureId = sqp.UUid(uniquegrp="perspicunique")
     PersonId = sqp.UUid(uniquegrp="perspicunique")
     Picture = sqp.JoinedEmbeddedObject(targettype=Picture, localid="pictureid", autofill=True)

     def __str__(self):
          return "[{}] {}".format(self.picture.readableid, self.picture.title)

class PictureToPersonSel(Picture):
     PersInter = sqp.JoinedEmbeddedObject(targettype=PersonPictureInter, localid="_id", foreignid="pictureid", autofill=True)


class Person(sqp.PBase):
     Name = sqp.String()
     FirstName = sqp.String()
     BioSex = sqp.Catalog(catalogtype=SexCat)
     NameOfBirth = sqp.String()
     Birthdate = sqp.DateTime()
     DeathDate = sqp.DateTime()
     FatherId = sqp.UUid()
     MotherId = sqp.UUid()
     Infotext = sqp.String()
     InfoBits = sqp.JoinedEmbeddedList(targettype=PersonInfoBit, foreignid=PersonInfoBit.TargetId, cascadedelete=True)
     Documents = sqp.IntersectedList(targettype=PersonDocumentInter, interupid="personId", interdownid="documentid")
     Pictures = sqp.IntersectedList(targettype=PersonPictureInter, interupid="personid", interdownid="pictureid")

     def __str__(self):
          if self.birthdate is not None:
               return "{0} {1} ({2:%d.%m.%Y})".format(self.firstname, self.name, self.birthdate)
          else:
               return "{0} {1}".format(self.firstname, self.name)



class DocumentInfoBit(_InfoBit):
     pass

class Document(sqp.PBase):
     ReadableId = sqp.String()
     Title = sqp.String(default="<Titel>")
     FilePath = sqp.String()
     Ext = sqp.String()
     ScanDate = sqp.DateTime()
     Type = sqp.Catalog(catalogtype=DocType)
     ProductionDate = sqp.DateTime()
     DocInfoBits = sqp.JoinedEmbeddedList(targettype=DocumentInfoBit, foreignid=DocumentInfoBit.TargetId, cascadedelete=True)

     def __str__(self):
          return "[{}] {} {} {}".format(self.readableid, 
                                      ewn(self.type), 
                                      ewn(self.productiondate),
                                      ewn(self.title))

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
     else:
          raise Exception("Unbekannter Datentyp in PersistClasses.py ewn()")
         