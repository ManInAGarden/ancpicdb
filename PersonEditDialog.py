import GeneratedGUI as gg
from PersistClasses import Person

class PersonEditDialog(gg.gPersonEditDialog):
    def __init__(self, parent, fact, dta : Person):
        super().__init__(parent)
        self._fact = fact
        self._person = dta

    def showmodal(self):
        if self._person != None:
            self._filldialog(self._person)

        return self.ShowModal()
    
    def _filldialog(self, p):
        self.m_NameTB.SetValue(p.name)
        self.m_vornameTB.SetValue(p.firstname)

    def flushnget(self):
        self._person.firstname = self.m_vornameTB.GetValue()
        self._person.name = self.m_NameTB.GetValue()
        self._fact.flush(self._person)
        return self._person
