import datetime
from FilterData import FilterData
from PictureFilterData import PictureFilterData
import sqlitepersist as sqp
from PersistClasses import Document

class DocumentFilterData(PictureFilterData):
    """A filter data class to be used with documents
        documents are basically the same as pictures with
        just one additional field to be filtered.
        Also those fluffy fields do not (yet) exist, so we can only search for
        the exact production date for now
    """

    def __init__(self, fact : sqp.SQFactory):
        super().__init__(fact)
        self.doctype = None
        self.proddate = None

    def get_info(self) -> str:
        answ = super().get_info()

        if self.doctype is not None and self.is_defined(self.doctype.value):
            answ += " UND Dokumentart='{}'".format(self.doctype.value)

        if self.proddate is not None:
            answ += " UND Produktionsdatum='{:%d.%m.%y}'".format(self.proddate)

        if answ.startswith(" UND "):
            answ = answ[5:]

        return answ
    
    def get_query(self) -> sqp.SQQuery:
        """create and return the query for the current filter"""
        q = sqp.SQQuery(self._fact, Document)

        # when a readable id is searched without wildcard (*) any other search is useless 
        # and will not be taken into account
        if self.is_strict(self.kennummer):
            return q.where(Document.ReadableId==self.kennummer)
        
        exp = None
        if self.is_defined(self.kennummer): #kennummer contains an asterix
            exp = self.add2exp(exp, sqp.IsLike(Document.ReadableId, self.kennummer.replace("*", "%")))
        
        if self.is_defined(self.title):
            if self.is_strict(self.title):
                exp = self.add2exp(exp, Document.Title==self.title)
            else:
                exp = self.add2exp(exp, sqp.IsLike(Document.Title, self.title.replace("*", "%")))

        if self.gruppe is not None:
            exp = self.add2exp(exp, Document.GroupId==self.gruppe._id)

        if self.doctype is not None:
            exp = self.add2exp(exp, Document.Type == self.doctype.code)

        if self.proddate is not None:
            exp = self.add2exp(exp, Document.ProductionDate == self.proddate)

        return q.where(exp).order_by(sqp.OrderInfo(Document.ScanDate, sqp.OrderDirection.DESCENDING))
    
    
