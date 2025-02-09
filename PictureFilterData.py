import sqlitepersist as sqp
from FilterData import FilterData
from PersistClasses import Picture
import datetime


class PictureFilterData(FilterData):
    """class to store filter data for pictures"""
    def __init__(self, fact : sqp.SQFactory):
        super().__init__(fact)
        self.kennummer = None
        self.title = None
        self.daytaken = None
        self.monthtaken = None
        self.yeartaken = None
        self.gruppe = None

    def get_info(self) -> str:
        answ = ""
        if self.is_defined(self.kennummer):
            answ += "Kenn#='" + self.kennummer + "'"

        if self.is_defined(self.title):
            answ += " UND Titel='{}'".format(self.title)

        if self.is_defined(self.daytaken):
            answ += " UND Aufnahmetag='{}'".format(self.daytaken)

        if self.is_defined(self.monthtaken):
            answ += " UND Aufnahmemonat='{}'".format(self.monthtaken)

        if self.is_defined(self.yeartaken):
            answ += " UND Aufnahmejahr='{}'".format(self.yeartaken)

        if self.gruppe is not None and self.is_defined(self.gruppe.name):
            answ += " UND Gruppe='{}'".format(self.gruppe.name)

        if answ.startswith(" UND "):
            answ = answ[5:]

        return answ
        
    def get_query(self) -> sqp.SQQuery:
        """create and return the query for the current filter"""
        q = sqp.SQQuery(self._fact, Picture)

        # when a readable id is searched without wildcard (*) any other search is useless 
        # and will not be taken into account
        if self.is_strict(self.kennummer):
            return q.where(Picture.ReadableId==self.kennummer)
        
        exp = None
        if self.is_defined(self.kennummer): #kennummer contains an asterix
            exp = self.add2exp(exp, sqp.IsLike(Picture.ReadableId, self.kennummer.replace("*", "%")))
        
        if self.is_defined(self.title):
            if self.is_strict(self.title):
                exp = self.add2exp(exp, Picture.Title==self.title)
            else:
                exp = self.add2exp(exp, sqp.IsLike(Picture.Title, self.title.replace("*", "%")))

        if self.gruppe is not None:
            exp = self.add2exp(exp, Picture.GroupId==self.gruppe._id)

        if self.is_strict(self.yeartaken) and self.is_strict(self.monthtaken) and self.is_strict(self.daytaken):
            yr = int(self.yeartaken)
            m = int(self.monthtaken)
            d = int(self.daytaken)
            exaktdt = datetime(yr, m, d)
            exp = self.add2exp(exp, Picture.TakenDate==exaktdt)
        else:
            if self.is_strict(self.yeartaken):
                exp = self.add2exp(exp, Picture.FlufTakenYear==self.yeartaken)
            
            if self.is_strict(self.monthtaken):
                m = int(self.monthtaken)
                mc = self._get_monthcode(m)
                exp = self.add2exp(exp, Picture.FlufTakenMonth==mc)

        return q.where(exp).order_by(sqp.OrderInfo(Picture.ScanDate, sqp.OrderDirection.DESCENDING))
    
    def get_query_info(self) -> str:
        if self.is_strict(self.kennummer):
            return "Kennung ist '{}'".format(self.kennummer)
        
        exps = None

        if self.is_defined(self.kennummer):
            self.add2exps(exps, "Kennung gleich '{}'".format(self.kennummer))

        if self.is_defined(self.title):
            if self.is_strict(self.title):
                exps = self.add2exps(exps, "Titel ist '{}'".format(self.title))
            else:
                exps = self.add2exps(exps, "Titel gleicht '{}'".format(self.title))

        if self.gruppe is not None:
            exps = self.add2exps(exps, "Gruppe ist '{}'".format(self.gruppe.name))

        if self.is_strict(self.yeartaken) and self.is_strict(self.monthtaken) and self.is_strict(self.daytaken):
            yr = int(self.yeartaken)
            m = int(self.monthtaken)
            d = int(self.daytaken)
            exaktdt = datetime(yr, m, d)
            exps = self.add2exps(exps, "Aufnahmedatum ist {:%d.%m.%Y}".format(exaktdt))
        else:
            if self.is_strict(self.yeartaken):
                exps = self.add2exps(exps, "aufgenommen im Jahr {}".format(self.yeartaken))
            
            if self.is_strict(self.monthtaken):
                exps = self.add2exps(exps, "aufgenommen im Monat {}".format(self.monthtaken))
                                     
        return exps
            
        

