import datetime
import copy
from dateutil.relativedelta import relativedelta
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, SexCat, FluffyMonthCat, PersonPictureInter, FullPerson
import sqlitepersist as sqp
from GuiHelper import GuiHelper
from AddPictureDialog import AddPictureDialog
from EditSignifcPictureDialog import EditSignifcPictureDialog

class PersonEditDialog(gg.gPersonEditDialog):

    def __init__(self, parent, fact, dta : Person):
        super().__init__(parent)
        self._fact = fact
        self._person = copy.copy(dta)
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

    def _get_other_parent(self, ch, par):
        """gets a string repr of the other parent of a child. Returns "Unbekannter Partner" if there's no other parent"""
        if ch.motherid != par._id:
            otherid = ch.motherid
        elif ch.fatherid != par._id:
            otherid = ch.fatherid
        else:
            otherid = None

        if otherid is None:
            return "Unbekannter Partner"
        
        otherpar = sqp.SQQuery(self._fact, Person).where(Person.Id == otherid).first_or_default(None)

        return otherpar.as_string()

    def _bdaykey(self, p):
        by = p.cons_birth_year
        if by is None:
            by = datetime.date.today().year

        return by

    def _get_children_nodes(self, p : Person):
        """returns a dictionary with partners as top nodes and children as subnodes"""
        fullp = sqp.SQQuery(self._fact, FullPerson).where(FullPerson.Id==p._id).first_or_default(None)
        self._fact.fill_joins(fullp,
                              FullPerson.ChildrenAsFather,
                              FullPerson.ChildrenAsMother)
        if fullp is None:
            raise Exception("Unbehandelte Ausnahme. FullPerson nicht gefunden in _get_children")
        
        allchildren = fullp.childrenasfather + fullp.childrenasmother
        allchildren.sort(key=self._bdaykey)
        answ = {}

        for child in allchildren:
            par = self._get_other_parent(child, p)
            if par not in answ:
                answ[par] = {}

            answ[par][child.as_string()] = None

        return answ


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
        
        if p._id is not None:
            #searching for children only works when p has already been saved to the db
            pns = self._get_children_nodes(self._person)
            GuiHelper.add_nodes(self.m_partners_childrenTCTRL, pns)

        self._fillpicturelist(p)
        
        self._tune_fluffies()

        #now fill mother and father
        #manipulate combo-boxes so that only older persons can be selected and not the person himself can be selected
        cmina = self.Parent.configuration.get_value("gui", "minageforparent")
        cmaxa = self.Parent.configuration.get_value("gui", "maxageforparent")
        if cmina is None: cmina = 16 #defaults
        if cmaxa is None: cmaxa = 70

        if p.birthdate is not None:
            bd = p.birthdate
        elif p.birthyear is not None and p.birthyear > 0:
            if p.birthmonth is not None and p.birthmonth.code != "NOMONTH":
                bm = p.birthmonth.as_number()
                bd = datetime.datetime(p.birthyear, bm, 12)
            else: 
                bd = datetime.datetime(p.birthyear, 12, 31)
        else:
            bd = None

        if bd is not None: #we have at least a birthyear
            refdate = bd - relativedelta(years=cmina)
            minrefdate = bd - relativedelta(years=cmaxa)
            refyear = refdate.year
            minrefyear = minrefdate.year
        
            #fill mother and father combos by only selecting persons that may be parents of the current person
            q = sqp.SQQuery(self._fact, Person).where(
                                                        (
                                                            (
                                                                sqp.IsNone(Person.Birthdate) & ((sqp.IsNone(Person.BirthYear)) | (Person.BirthYear == 0))
                                                            )
                                                        |
                                                        (
                                                            (
                                                                (Person.Birthdate < refdate) | ((Person.BirthYear < refyear) & (Person.BirthYear>0))
                                                            )
                                                            &
                                                            (
                                                                (Person.Birthdate > minrefdate) | (Person.BirthYear > minrefyear)
                                                            )
                                                        )
                                                     )
                                                     & (Person.BioSex == "MALE")).order_by(Person.FirstName)
            self._pfathers = list(q) #remember possible fathers for selection change
        
            q = sqp.SQQuery(self._fact, Person).where((
                                                            (
                                                                sqp.IsNone(Person.Birthdate) & ((sqp.IsNone(Person.BirthYear)) | (Person.BirthYear == 0))
                                                            )
                                                        |
                                                        (
                                                            (
                                                                (Person.Birthdate < refdate) | ((Person.BirthYear < refyear) & (Person.BirthYear>0))
                                                            )
                                                            &
                                                            (
                                                                (Person.Birthdate > minrefdate) | (Person.BirthYear > minrefyear)
                                                            )
                                                        )
                                                     )
                                                     & (Person.BioSex == "FEMALE")).order_by(Person.FirstName)
            self._pmothers = list(q) #rember possible mothers for selection change
        else: #we have no hint when the person was born so we need to offer any other person as mother or father
            self._pfathers = sqp.SQQuery(self._fact, Person).where(Person.BioSex=="MALE").as_list()
            self._pmothers = sqp.SQQuery(self._fact, Person).where(Person.BioSex=="FEMALE").as_list()

        #make sure any already connected father or mother is in the list.
        self._pfathers = self._assurecontains(self._pfathers, p.fatherid)
        self._pmothers = self._assurecontains(self._pmothers, p.motherid)

        pfs = self._get_strlist(self._pfathers)
        self.m_fatherCB.Set(pfs)
        fatherp = self._getfirst_personidx(self._pfathers, p.fatherid)
        if fatherp is not wx.NOT_FOUND:
            self.m_fatherCB.Select(fatherp)

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
            else:
                self._person.motherid = None

        if len(self._pfathers)>0:
            fatherp = self.m_fatherCB.GetSelection()
            if fatherp is not wx.NOT_FOUND:
                self._person.fatherid = self._pfathers[fatherp]._id
            else:
                self._person.fatherid = None

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

    def removeFatherLink(self, event):
        if self._person.fatherid is None:
            return
        
        self.m_fatherCB.SetSelection(wx.NOT_FOUND)
    

    def removeMotherLink(self, event):
        if self._person.motherid is None:
            return
        
        self.m_motherCB.SetSelection(wx.NOT_FOUND)
