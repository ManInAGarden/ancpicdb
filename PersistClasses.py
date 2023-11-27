import sqlitepersist as sqp


class _InfoBit(sqp.PBase):
     TargetId = sqp.UUid()
     InfoContent = sqp.String()

class PersonInfoBit(_InfoBit):
     """class for informations according persons"""
     pass

class PersonDocumentInter(sqp.PBase):
     """intersection of Person and Documents"""
     DocumentId = sqp.UUid()
     PersonId = sqp.UUid()

class PersonPictureInter(sqp.PBase):
     PictureId = sqp.UUid()
     PersonId = sqp.UUid()

class Person(sqp.PBase):
     Name = sqp.String()
     FirstName = sqp.String()
     NameOfBirth = sqp.String()
     Birthdate = sqp.DateTime()
     FatherId = sqp.UUid()
     MotherId = sqp.UUid()
     Infotext = sqp.String()
     InfoBits = sqp.JoinedEmbeddedList(targettype=PersonInfoBit, foreignid=PersonInfoBit.TargetId, cascadedelete=True)
     Documents = sqp.IntersectedList(targettype=PersonDocumentInter, interupid=PersonDocumentInter.PersonId, interdownid=PersonDocumentInter.DocumentId)
     Pictures = sqp.IntersectedList(targettype=PersonPictureInter, interupid=PersonPictureInter.PersonId, interdownid=PersonPictureInter.PictureId)

     def __str__(self):
          return "{0} {1}".format(self.vorname, self.name)

class PictureInfoBit(_InfoBit):
     """class for informations according pictures"""
     pass

class Picture(sqp.PBase):
     """class for pictures normally with people on them"""
     ReadableId = sqp.String()
     FilePath = sqp.String()
     ScanDate = sqp.DateTime()
     TakenDate = sqp.DateTime()
     Title = sqp.String()
     SettledInformation = sqp.String()
     PictInfoBits = sqp.JoinedEmbeddedList(targettype=PictureInfoBit, foreignid=PictureInfoBit.TargetId, cascadedelete=True)

class DocumentInfoBit(_InfoBit):
     pass

class Document(sqp.PBase):
     ReadableId = sqp.String()
     FilePath = sqp.String()
     ScanDate = sqp.DateTime()
     Type = sqp.String()
     ProductionDate = sqp.DateTime()
     DocInfoBits = sqp.JoinedEmbeddedList(targettype=DocumentInfoBit, foreignid=DocumentInfoBit.TargetId, cascadedelete=True)





