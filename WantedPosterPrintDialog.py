import copy
import os
import tempfile as tmpf
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, FullPerson
import sqlitepersist as sqp
from GuiHelper import GuiHelper
from WantedPoster import WantedPoster
from DocArchiver import DocArchiver

def getbm(mocode : str):
    mos = ["NOMONTH",
           "MONTH01", 
           "MONTH02", 
           "MONTH03", 
           "MONTH04", 
           "MONTH05", 
           "MONTH06", 
           "MONTH07", 
           "MONTH08", 
           "MONTH09", 
           "MONTH10", 
           "MONTH11", 
           "MONTH12"]
    
    return mos.index(mocode)
    

class WantedPosterPrintDialog(gg.gWantedPosterPrintDialog):

    class WantedConfig(object):
        @property
        def posterconf(self):
            return self._posterconf
        
        @property
        def handledpers(self):
            return self._handledpers
        
        
        def __init__(self):
            self._handledpers = []
            self._posterconf = WantedPoster.PosterConfig()
            self._archpath = None
           
    @property
    def wpconf(self):
        return self._wpconf
    
    def __init__(self, parent, fact : sqp.SQFactory, archiver : DocArchiver, conf : WantedConfig):
        super().__init__(parent)
        self._fact = fact
        tdir = tmpf.gettempdir()
        self._configuration = parent.configuration
        self._archiver = archiver
        self._localarchtemp = tdir + os.path.sep + self._configuration.get_value("archivestore", "localtemp")

        self._wpconf = copy.deepcopy(conf)
        self._allpersons = self._get_all_persons()

    def _get_sort_key(self, p):
        fname = p.firstname
        lname = p.name
        
        if fname is None: fname = ""
        if lname is None: lname = ""

        if p.birthdate is not None:
            by = p.birthdate.year
            bm = p.birthdate.month
            bd = p.birthdate.day
        else:
            bd = 0
            if p.birthyear is not None:
                by = p.birthyear
            else:
                by = 0
            if p.birthmonth is not None:
                bm = getbm(p.birthmonth.code)
            else:
                bm = 0

        return (lname, fname, by, bm, bd)
    
    def _get_all_persons(self):
        persons = sqp.SQQuery(self._fact, Person).order_by(Person.Name, Person.FirstName, Person.Birthdate).as_list()
        persons.sort(key=self._get_sort_key)
        return persons

    def _contains(self, persons : list, p : Person) -> bool:
        for pers in persons:
            if pers._id == p._id:
                return True
        
        return False
    
    def _fillplist(self):
        ct = -1
        ps = []
        seli = []
        for p in self._allpersons:
            ps.append(p.as_string())
            ct += 1
            if self._contains(self._wpconf._handledpers, p):
                seli.append(ct)

        self.m_personsCHLB.Clear()
        self.m_personsCHLB.InsertItems(ps, 0)
        self.m_personsCHLB.SetCheckedItems(seli)
        
    def _fill_gui(self):
        self._fillplist()
        GuiHelper.set_val(self.m_newPagePerPersoneCB, self._wpconf.posterconf.newpgperperson)
        GuiHelper.set_val(self.m_addSignificantPicturesCB, self._wpconf.posterconf.includepics)
        GuiHelper.set_val(self.m_targetFileFPI, self._wpconf.posterconf.targetfile)

    def _refresh_handled_persons(self):
        checkits = self.m_personsCHLB.GetCheckedItems()
        self._wpconf._handledpers = []
        for checki in checkits:
            self._wpconf._handledpers.append(self._allpersons[checki])


    def showmodal(self):
        self._fill_gui()
        res = self.ShowModal()

        if res != wx.ID_OK:
            return res
        
        self._refresh_wpconfig()        
        self._refresh_handled_persons()

        return res
        
    def _refresh_wpconfig(self):
        self._wpconf.posterconf.newpgperperson = GuiHelper.get_val(self.m_newPagePerPersoneCB)
        self._wpconf.posterconf.includepics = GuiHelper.get_val(self.m_addSignificantPicturesCB)
        self._wpconf.posterconf.targetfile = GuiHelper.get_val(self.m_targetFileFPI)

    def doClose(self, event):
        self.EndModal(wx.ID_OK)

    def doPrinting(self, event):
        self._refresh_handled_persons()
        fullps = []
        for pers in self._wpconf._handledpers:
            #get current person as FullPerson and fill it's joins to get the person's full data for printing
            fullp = sqp.SQQuery(self._fact, FullPerson).where(FullPerson.Id==pers._id).first_or_default(None)
            self._fact.fill_joins(fullp,
                                  FullPerson.Father,
                                  FullPerson.Mother,
                                  FullPerson.ChildrenAsFather,
                                  FullPerson.ChildrenAsMother,
                                  FullPerson.Pictures)
            if fullp is None:
                raise Exception("Unbehandelte Ausnahme. FullPerson nicht gefunden in doPrinting")
            fullps.append(fullp)

        self._refresh_wpconfig()
        wp = WantedPoster(fullps, 
                          self._archiver, 
                          self._localarchtemp,
                          self._wpconf.posterconf)
        wp.do_create()
        
