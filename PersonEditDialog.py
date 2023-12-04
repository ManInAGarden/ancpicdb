import datetime
from dateutil.relativedelta import relativedelta
import wx
import wx.adv
import GeneratedGUI as gg
from PersistClasses import Person, SexCat
import sqlitepersist as sqp

class PersonEditDialog(gg.gPersonEditDialog):
    def __init__(self, parent, fact, dta : Person):
        super().__init__(parent)
        self._fact = fact
        self._person = dta

    def showmodal(self):
        if self._person != None:
            self._filldialog(self._person)

        return self.ShowModal()
    
    def _set_val(self, ctrl, val):
        """set value if not none"""

        ct = type(ctrl)
        if ct is wx.TextCtrl:
            if val is not None:
                ctrl.SetValue(val)
            else:
                ctrl.SetValue("")
        elif ct is wx.adv.DatePickerCtrl:
            if val is not None:
                ctrl.SetValue(wx.pydate2wxdate(val))
            else:
                ctrl.SetValue(wx.InvalidDateTime)
        else:
            raise Exception("Unknown control type in _set_val")
        
    def _get_val(self, ctrl):
        ctt = type(ctrl)
        if ctt is wx.adv.DatePickerCtrl:
            val = ctrl.GetValue()
            if val is wx.InvalidDateTime:
                return None
            else:
                return wx.wxdate2pydate(val)
        elif ctt is wx.TextCtrl:
            val = ctrl.GetValue()
            if val is None or len(val)==0:
                return None
            else:
                return val
        else:
            raise Exception("Unknown type {} in _get_val()".format(ctt))

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
            
    def _filldialog(self, p):
        self._set_val(self.m_NameTB, p.name)
        self._set_val(self.m_vornameTB, p.firstname)
        self._set_val(self.m_geburtsnameTB, p.nameofbirth)
        self._set_val(self.m_infotextTB, p.infotext)
        self._set_val(self.m_geburtsdatumDP, p.birthdate)
        self._set_val(self.m_todesdatumDP, p.deathdate)
        
        #now fill mother and father
        #manipulate combo-boxes so that only older persons can be selected and not the person himself can be selected
        if p.birthdate is not None:
            cdd = self.Parent.configuration.get_value("gui", "childdeltayears")
            if cdd is None: cdd = 16
            refdate = p.birthdate - relativedelta(years=cdd)
        else:
            refdate = datetime.datetime.today()

        #fill biosex combo
        q = sqp.SQQuery(self._fact, SexCat).where(SexCat.LangCode=="DEU").order_by(SexCat.Value)
        self._biosexes = list(q)
        bios = self._get_catdisplay_list(self._biosexes) #rember the biosexes for selection change
        self.m_bioSexCB.Set(bios)
        
        biosexp = self._get_first_biosexidx(p.biosex)
        if biosexp is not wx.NOT_FOUND:
            self.m_bioSexCB.Select(biosexp)

        #fill mother and father combos
        q = sqp.SQQuery(self._fact, Person).where((Person.Birthdate < refdate) & (Person.BioSex == "MALE")).order_by(Person.FirstName)
        self._pfathers = list(q) #rember possible fathers for selection change
        self._pfathers = self._assurecontains(self._pfathers, self._person.fatherid)
        pfs = self._get_strlist(self._pfathers)
        self.m_fatherCB.Set(pfs)
        fatherp = self._getfirst_personidx(self._pfathers, p.fatherid)
        if fatherp is not wx.NOT_FOUND:
            self.m_fatherCB.Select(fatherp)

        q = sqp.SQQuery(self._fact, Person).where((Person.Birthdate < refdate) & (Person.BioSex == "FEMALE")).order_by(Person.FirstName)
        self._pmothers = list(q) #rember possible mothers for selection change
        self._pmothers = self._assurecontains(self._pmothers, self._person.motherid)
        pms = self._get_strlist(self._pmothers)
        self.m_motherCB.Set(pms)
        motherp = self._getfirst_personidx(self._pmothers, p.motherid)
        if motherp is not wx.NOT_FOUND:
            self.m_motherCB.Select(motherp)


    def flushnget(self):
        self._person.firstname = self._get_val(self.m_vornameTB)
        self._person.name = self._get_val(self.m_NameTB)
        self._person.birthdate = self._get_val(self.m_geburtsdatumDP)
        self._person.deathdate = self._get_val(self.m_todesdatumDP)
        self._person.infotext = self._get_val(self.m_infotextTB)
        self._person.nameofbirth = self._get_val(self.m_geburtsnameTB)

        biosexp = self.m_bioSexCB.GetSelection()
        if biosexp is not wx.NOT_FOUND:
            self._person.biosex = self._biosexes[biosexp]

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
