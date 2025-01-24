import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import Picture, PersonPictureInter_Hollow

class ConnectedPersonsDialog(gg.gConnectedPersonsDialog):
    CONNDEFINS = [
            {"propname" : "personid", "title": "PersonenID", "width":100},
            {"propname" : "person.firstname", "title": "Vorname", "width":130},
            {"propname" : "person.name", "title": "Nachname", "width":130},
            {"propname" : "person.cons_birth_year", "title": "Geburtstag"}
    ]
    def __init__(self, parent, fact : sqp.SQFactory, picture : Picture):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._picture = picture
        self._set_list_columns()


    def _set_list_columns(self):
        GuiHelper.set_columns_forlstctrl(self.m_connectionsLCTRL, self.CONNDEFINS)
    
    def showmodal(self):
        
        self._fill_dialog()
        res = self.ShowModal()

    def _fill_dialog(self):
        p = self._picture

        GuiHelper.set_val(self.m_pictureIdTB, p.readableid)
        GuiHelper.set_val(self.m_pictureNameTB, p.title)
        self._perspicints = sqp.SQQuery(self._fact, PersonPictureInter_Hollow).where(PersonPictureInter_Hollow.PictureId==p._id).as_list()
        for pers in self._perspicints:
            try:
                self._fact.fill_joins(pers, PersonPictureInter_Hollow.Person)
            except:
                pass

        GuiHelper.set_data_for_lstctrl(self.m_connectionsLCTRL,
                                       self.CONNDEFINS,
                                       self._perspicints)



    def removePersonConn(self, event):
        selconn = GuiHelper.get_selected_fromlctrl(self.m_connectionsLCTRL, self._perspicints)
        if selconn is None: return

        res = GuiHelper.ask_user(self, "Wirklich die Verbindung zur markierten Person (Id={}) entfernen?".format(selconn.personid))

        if res != wx.ID_YES: return

        self._fact.delete(selconn)
        self._fill_dialog()

    def addPersonConn(self, event):
        pass