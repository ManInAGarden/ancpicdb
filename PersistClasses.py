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

     def __str__(self):
          return "[{}] {}".format(self.picture.readableid, self.picture.title)

#class PictureToPersonSel(Picture):
#     PersInter = sqp.JoinedEmbeddedObject(targettype=PersonPictureInter, localid="_id", foreignid="pictureid", autofill=True)


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
          answ = "{0} {1}".format(self.firstname, self.name)

          if self.birthdate is not None:
               answ += ": *{:%d.%m.%Y}".format(self.birthdate)
          
          if self.deathdate is not None:
               answ += ", +{:%d.%m.%Y}".format(self.deathdate)
          
          return answ


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
         