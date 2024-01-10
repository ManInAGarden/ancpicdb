import datetime
from dateutil.relativedelta import relativedelta
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, SexCat, FluffyMonthCat, PersonPictureInter
import sqlitepersist as sqp
from GuiHelper import GuiHelper
from AddPictureDialog import AddPictureDialog
from EditSignifcPictureDialog import EditSignifcPictureDialog

class PersonEditDialog(gg.gPersonEditDialog):
    def __init__(self, parent, fact, dta : Person):
        super().__init__(parent)
        self._fact = fact
        self._person = dta
        self._configuration = parent.configuration
        self._init_gui()
        

    def _init_gui(self):
        self._init_cats()
        self.m_significantPictursLCTRL.ClearAll()        
        self.m_significantPictursLCTRL.InsertColumn(0, "Position")
        self.m_significantPictursLCTRL.InsertColumn(1, "Untertitel", width=300)
        self.m_significantPictursLCTRL.InsertColumn(2, "Kennung")
        self.m_significantPictursLCTRL.InsertColumn(3, "Titel")


    def _init_cats(self):
        #fluffymonth combo (new way of initializing)
        q = sqp.SQQuery(self._fact, FluffyMonthCat).where(FluffyMonthCat.LangCode=="DEU").order_by(FluffyMonthCat.Code)
        self._flufmonths = q.as_list()

        #biosexes
        q = sqp.SQQuery(self._fact, SexCat).where(SexCat.LangCode=="DEU").order_by(SexCat.Value)
        self._biosexes = list(q)

    def showmodal(self):
        if self._person != None:
            self._filldialog(self._person)

        return self.ShowModal()
    
    
    def _get_strlist(self, itera):
        answ = []
        for p in itera:
            ps = p.__str__()
            answ.append(ps)
        
        return answ
    
    def _get_catdisplay_list(self, vals : sqp.PCatalog):
        answ = []
        for val in vals:
            valstr = val.value
            answ.append(valstr)

        return answ
    
    def _get_first_biosexidx(self, val):
        if val is None:
            return wx.NOT_FOUND
        
        for i in range(len(self._biosexes)):
            if val.value==self._biosexes[i].value:
                return i
        
        return wx.NOT_FOUND

    def _getfirst_personidx(self, plist, pid):
        if pid is None:
            return wx.NOT_FOUND
        
        for i in range(len(plist)):
            if plist[i]._id == pid:
                return i
            
        return wx.NOT_FOUND
    
    def _assurecontains(self, perslist, personid):
        if personid is None:
            return perslist
        
        for p in perslist:
            if p._id == personid:
                return perslist
            
        mustpers = sqp.SQQuery(self._fact, Person).where(Person.Id==personid).first_or_default(None)
        #mustpers = self._fact.find(Person, personid)

        return perslist + [mustpers]
    
    def _tune_fluffies(self):
        bdate = GuiHelper.get_val(self.m_geburtsdatumDP)
        if bdate is None:
            self.m_fluffyMonthCB.Enable()
            self.m_fluffyYearSPC.Enable()
        else:
            self.m_fluffyMonthCB.Disable()
            self.m_fluffyYearSPC.Disable()

        ddate = GuiHelper.get_val(self.m_todesdatumDP)
        if ddate is None:
            self.m_fluffyDeathMonthCB.Enable()
            self.m_fluffyDeathYearSPC.Enable()
        else:
            self.m_fluffyDeathMonthCB.Disable()
            self.m_fluffyDeathYearSPC.Disable()

    def _getmonthnumber(self, mocode):
        mocodes = ["MONTH01", "MONTH02", "MONTH03", "MONTH04", "MONTH05", "MONTH06", 
                   "MONTH07", "MONTH08", "MONTH09", "MONTH10", "MONTH11", "MONTH12"]
        return mocodes.index(mocode) + 1
    
    def _fillpicturelist(self, p : Person):
        ctrl = self.m_significantPictursLCTRL
        ctrl.DeleteAllItems()
        self._fact.fill_joins(p, Person.Pictures)

        ct = 0
        for pic in p.pictures:
            idx = ctrl.InsertItem(ctrl.GetColumnCount(), GuiHelper.get_eos(pic.position))
            ctrl.SetItemData(idx, ct)
            ctrl.SetItem(idx, 1, GuiHelper.get_eos(pic.subtitle))
            ctrl.SetItem(idx, 2, GuiHelper.get_eos(pic.picture.readableid))
            ctrl.SetItem(idx, 3, GuiHelper.get_eos(pic.picture.title))
            ct += 1

    def _filldialog(self, p):
        GuiHelper.set_val(self.m_NameTB, p.name)
        GuiHelper.set_val(self.m_vornameTB, p.firstname)
        GuiHelper.set_val(self.m_rufnameTB, p.rufname)
        GuiHelper.set_val(self.m_geburtsnameTB, p.nameofbirth)
        GuiHelper.set_val(self.m_infotextTB, p.infotext)
        GuiHelper.set_val(self.m_geburtsdatumDP, p.birthdate)
        GuiHelper.set_val(self.m_todesdatumDP, p.deathdate)
        GuiHelper.set_val(self.m_bioSexCB, p.biosex, self._biosexes)
        GuiHelper.set_val(self.m_fluffyMonthCB, p.birthmonth, self._flufmonths)
        GuiHelper.set_val(self.m_fluffyYearSPC, p.birthyear)
        GuiHelper.set_val(self.m_fluffyDeathMonthCB, p.deathmonth, self._flufmonths)
        GuiHelper.set_val(self.m_fluffyDeathYearSPC, p.deathyear, self._flufmonths)
        
        self._fillpicturelist(p)
        
        self._tune_fluffies()

        #now fill mother and father
        #manipulate combo-boxes so that only older persons can be selected and not the person himself can be selected
        cdd = self.Parent.configuration.get_value("gui", "childdeltayears")
        if cdd is None: cdd = 16
        
        if p.birthdate is not None:
            bd = p.birthdate
        elif p.birthyear is not None and p.birthyear > 0:
            if p.birthmonth is not None and p.birthmonth.code != "NOMONTH":
                bm = self._getmonthnumber(p.birthmonth.code)
                bd = datetime.datetime(p.birthyear, bm, 12)
            else: 
                bd = datetime.datetime(p.birthyear, 12, 31)
        else:
            bd = datetime.datetime.today()

        refdate = bd - relativedelta(years=cdd)
        refyear = refdate.year
        
        #fill mother and father combos
        q = sqp.SQQuery(self._fact, Person).where(((Person.Birthdate < refdate) 
                                                    | (Person.BirthYear < refyear)
                                                    | (sqp.IsNone(Person.Birthdate)))
                                                  & (Person.BioSex == "MALE")).order_by(Person.FirstName)
        self._pfathers = list(q) #rember possible fathers for selection change
        self._pfathers = self._assurecontains(self._pfathers, p.fatherid)
        pfs = self._get_strlist(self._pfathers)
        self.m_fatherCB.Set(pfs)
        fatherp = self._getfirst_personidx(self._pfathers, p.fatherid)
        if fatherp is not wx.NOT_FOUND:
            self.m_fatherCB.Select(fatherp)

        q = sqp.SQQuery(self._fact, Person).where(((Person.Birthdate < refdate) 
                                                    | (Person.BirthYear < refyear)
                                                    | (sqp.IsNone(Person.Birthdate))) 
                                                    & (Person.BioSex == "FEMALE")).order_by(Person.FirstName)
        self._pmothers = list(q) #rember possible mothers for selection change
        self._pmothers = self._assurecontains(self._pmothers, self._person.motherid)
        pms = self._get_strlist(self._pmothers)
        self.m_motherCB.Set(pms)
        motherp = self._getfirst_personidx(self._pmothers, p.motherid)
        if motherp is not wx.NOT_FOUND:
            self.m_motherCB.Select(motherp)


    def birthDateChanged(self, event):
        self._tune_fluffies()

    def deathDateChanged(self, event):
        self._tune_fluffies()

    def flushnget(self):
        p = self._person
        p.firstname = GuiHelper.get_val(self.m_vornameTB)
        p.name = GuiHelper.get_val(self.m_NameTB)
        p.rufname = GuiHelper.get_val(self.m_rufnameTB)
        p.birthdate = GuiHelper.get_val(self.m_geburtsdatumDP)
        p.deathdate = GuiHelper.get_val(self.m_todesdatumDP)
        p.infotext = GuiHelper.get_val(self.m_infotextTB)
        p.nameofbirth = GuiHelper.get_val(self.m_geburtsnameTB)
        p.biosex = GuiHelper.get_val(self.m_bioSexCB, self._biosexes)
        p.birthmonth = GuiHelper.get_val(self.m_fluffyMonthCB, self._flufmonths)
        p.birthyear = GuiHelper.get_val(self.m_fluffyYearSPC)
        p.deathmonth = GuiHelper.get_val(self.m_fluffyDeathMonthCB, self._flufmonths)
        p.deathyear = GuiHelper.get_val(self.m_fluffyDeathYearSPC)
        
        if len(self._pmothers)>0:
            motherp = self.m_motherCB.GetSelection()
            if motherp is not wx.NOT_FOUND:
                self._person.motherid = self._pmothers[motherp]._id

        if len(self._pfathers)>0:
            fatherp = self.m_fatherCB.GetSelection()
            if fatherp is not wx.NOT_FOUND:
                self._person.fatherid = self._pfathers[fatherp]._id

        self._fact.flush(self._person)
        return self._person
    
    def addPicture(self, event):
        """add a picture to the person"""
        
        p = self._person
        dial = AddPictureDialog(self, self._fact, p)
        res = dial.showmodal()

        if res == wx.ID_OK:
            for pic in dial.selection:
                persinterpic = PersonPictureInter(personid=p._id,
                                                  pictureid=pic._id)
                self._fact.flush(persinterpic)

        p.pictures = None #that means a new select wirll be done by the following fill_joins
        self._fact.fill_joins(p, Person.Pictures)
        self._fillpicturelist(p)

    def removePicture(self, event):
        p = self._person
        selpicinter = GuiHelper.get_selected_fromlctrl(self.m_significantPictursLCTRL, p.pictures)
        if selpicinter is None:
            return
        
        res = GuiHelper.ask_user(self, 
                                 "Soll das Bild '{}' wirklich von der Person abgetrennt werden?".format(selpicinter.picture.readableid))
        if res != wx.ID_YES:
            return
        
        self._fact.delete(selpicinter)
        p.pictures = None #that means a new select wirll be done by the following fill_joins
        self._fact.fill_joins(p, Person.Pictures)
        self._fillpicturelist(p)

    def editPictureInfo(self, event):
        p = self._person
        selpicinter = GuiHelper.get_selected_fromlctrl(self.m_significantPictursLCTRL, p.pictures)
        if selpicinter is None:
            return
        
        picintdial = EditSignifcPictureDialog(self, self._fact, selpicinter)
        res = picintdial.showmodal()
        #flushing of intersection is done by the dialog itself, but wen need to to some refreshs here
        p.pictures = None #that means a new select wirll be done by the following fill_joins
        self._fact.fill_joins(p, Person.Pictures)
        self._fillpicturelist(p)