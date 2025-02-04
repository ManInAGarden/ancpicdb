import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
import sqlitepersist as sqp
from PersistClasses import Picture, PersonPictureInter_Hollow, Document, PersonDocumentInter_Hollow

class ConnectedPersonsDialog(gg.gConnectedPersonsDialog):
    CONNDEFINS = [
            {"propname" : "personid", "title": "PersonenID", "width":100},
            {"propname" : "person.firstname", "title": "Vorname", "width":130},
            {"propname" : "person.name", "title": "Nachname", "width":130},
            {"propname" : "person.cons_birth_year", "title": "Geburtstag"}
    ]
    def __init__(self, parent, fact : sqp.SQFactory, dataobj : object):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._persints = None

        if type(dataobj) is Picture:
            self._type = "PIC"
            self._picture = dataobj
            self._document = None
        elif type(dataobj) is Document:
            self._type = "DOC"
            self._picture = None
            self._document = dataobj
        else:
            raise Exception("Unknown data type in ConnectedPersonsDialog")
        
        self._set_list_columns()


    def _set_list_columns(self):
        GuiHelper.set_columns_forlstctrl(self.m_connectionsLCTRL, self.CONNDEFINS)
    
    def showmodal(self):
        self._fill_dialog()
        res = self.ShowModal()

    def _get_persints(self):
        persints = None
        if self._type == "PIC":
            pi = self._picture
            persints = sqp.SQQuery(self._fact, PersonPictureInter_Hollow).where(PersonPictureInter_Hollow.PictureId==pi._id).as_list()
            for pers in persints:
                try:
                    self._fact.fill_joins(pers, PersonPictureInter_Hollow.Person)
                except:
                    pass
        elif self._type =="DOC":
            pi = self._document
            persints = sqp.SQQuery(self._fact, PersonDocumentInter_Hollow).where(PersonDocumentInter_Hollow.DocumentId==pi._id).as_list()
            for pers in persints:
                try:
                    self._fact.fill_joins(pers, PersonDocumentInter_Hollow.Person)
                except:
                    pass
        

        return persints

    def _data_obj(self):
        p = None
        if self._type=="PIC":
            p = self._picture
        elif self._type == "DOC":
            p = self._document
        else:
            raise Exception("Inknown type in ConnectedPersonsDialog")
        return p
    
    def _fill_dialog(self):
        dao = self._data_obj()

        GuiHelper.set_val(self.m_pictureIdTB, dao.readableid)
        GuiHelper.set_val(self.m_pictureNameTB, dao.title)
        
        self._persints = self._get_persints()

        GuiHelper.set_data_for_lstctrl(self.m_connectionsLCTRL,
                                       self.CONNDEFINS,
                                       self._persints)



    def removePersonConn(self, event):
        selconn = GuiHelper.get_selected_fromlctrl(self.m_connectionsLCTRL, self._persints)
        if selconn is None: return

        res = GuiHelper.ask_user(self, "Wirklich die Verbindung zur markierten Person (Id={}) entfernen?".format(selconn.personid))

        if res != wx.ID_YES: return

        self._fact.delete(selconn)
        self._fill_dialog()

    def addPersonConn(self, event):
        pass

    def connectionSelected(self, even):
        selconn = GuiHelper.get_selected_fromlctrl(self.m_connectionsLCTRL, self._persints)
        GuiHelper.enable_ctrls(selconn!=None, self.m_removePersonConnBU)

    def connectionDeselected(self, event):
        selconn = GuiHelper.get_selected_fromlctrl(self.m_connectionsLCTRL, self._persints)
        GuiHelper.enable_ctrls(selconn!=None, self.m_removePersonConnBU)