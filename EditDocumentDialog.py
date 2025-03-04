import tempfile as tmpf
import datetime
import copy
import wx
import wx.adv
from FindPersonsDialog import FindPersonsDialog
import sqlitepersist as sqp

from PersistClasses import Document, DocumentInfoBit, DocTypeCat, DataGroup, PersonDocumentInter_Hollow
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from EditInfoBitDialog import EditInfoBitDialog

class EditDocumentDialog(gg.geditDocumentDialog):
    DOCINFODEFINS = [
        {"propname" : "infodate", "title": "Datum", "format": "{:%d.%m.%Y}", "width":120},
        {"propname" : "suppliedby", "title": "Quelle", "width":150},
        {"propname" : "infocontent", "title": "Inhalt", "width": 340}
    ]

    CONNNPERSINFODEFINS =[
        #{"propname" : "_id", "title": "Id"},
        {"propname" : "person.firstname", "title": "Vorname"},
        {"propname" : "person.name", "title": "Name"},
        {"propname" : "person.cons_birth_year", "title": "Geburtsjahr"}
    ]


    @property
    def document(self): return self._document

    @property
    def configuration(self): return self._configuration

    def __init__(self, parent, fact : sqp.SQFactory, document : Document):
        super().__init__(parent)
        
        GuiHelper.set_icon(self)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self._document = copy.copy(document)
        self._docgroups = self._get_docgroups()
        self._temp = tmpf.gettempdir()
        self._create_lctrl_cols()

    def _get_docgroups(self):
        return sqp.SQQuery(self._fact, DataGroup).where(DataGroup.GroupType=="DOC").order_by(DataGroup.OrderNum).as_list()
        
    def _create_lctrl_cols(self):
        GuiHelper.set_columns_forlstctrl(self.m_zusatzinfoLCT, self.DOCINFODEFINS)
        GuiHelper.set_columns_forlstctrl(self.m_conPersoLCTRL, self.CONNNPERSINFODEFINS)


    def _fill_ibcols(self):
        if self._document.docinfobits is None: return

        GuiHelper.set_data_for_lstctrl(self.m_zusatzinfoLCT, 
                                       self.DOCINFODEFINS,
                                       self._document.docinfobits)
        
    def _fill_connpersons(self):
        self._connected_persons = sqp.SQQuery(self._fact, PersonDocumentInter_Hollow).where(
            PersonDocumentInter_Hollow.DocumentId == self._document._id).as_list()
        
        hadprob = False
        for hp in self._connected_persons:
            try:
                self._fact.fill_joins(hp, PersonDocumentInter_Hollow.Person)
            except:
                hadprob = True

        if hadprob:
            GuiHelper.show_error("Mindestens eine der mit dem Dokument verknüpften Personen exisitiert nicht (mehr) in der Datenbank. Bitte prüfe dies in der Dokumentenliste")

        GuiHelper.set_data_for_lstctrl(self.m_conPersoLCTRL, 
                                       self.CONNNPERSINFODEFINS, 
                                       self._connected_persons)

            
    def _get_all_types(self):
        return sqp.SQQuery(self._fact, DocTypeCat).where(DocTypeCat.Type=="DOC_TYPE").order_by(DocTypeCat.Value).as_list()
        
    def isempty(self, val):
        if val is None:
            return True
        
        if type(val) is str:
            if len(val)==0:
                return True
            
        return False
    
    def dgshow(self, arg):
        return arg.name
    
    def _filldialog(self):
        d = self._document
        self._fact.fill_joins(d, Document.DocInfoBits)
        self._doctypelist = self._get_all_types()
        GuiHelper.set_val(self.m_kennummerTB, d.readableid)
        GuiHelper.set_sqp_objval(self.m_groupCB, d.documentgroup, self.dgshow, self._docgroups)
        GuiHelper.set_val(self.m_doctypCB, d.type, fullcat=self._doctypelist)
        GuiHelper.set_val(self.m_titelTB, d.title)
        GuiHelper.set_val(self.m_scanDatumDP, d.scandate)
        GuiHelper.set_val(self.m_produktionsDatumDP, d.productiondate)
        GuiHelper.set_val(self.m_archivepathTB, d.filepath)
        GuiHelper.set_val(self.m_docextTB, d.ext)
        self._fill_ibcols()
        self._fill_connpersons()


    def _scaleimagetomax(self, img : wx.Image, width : int, height : int):
        """scale image so that it fits into a box with the given width and height without defomation """
        oriwi = img.GetWidth()
        orihe = img.GetHeight()
        wif = width / oriwi
        hef = height / orihe

        if wif <= hef:
            neww = int(wif * oriwi)
            newh = int(wif * orihe)
        else:
            neww = int(hef * oriwi)
            newh = int(hef * orihe)

        return img.Scale(width=neww, height=newh)

    def _get_unspec_type(self):
        return self._fact.getcat(DocTypeCat, "NSP")
    
    def showmodal(self):
        self._filldialog()

        res = self.ShowModal()

        if res == wx.ID_CANCEL:
            return res
        
        d = self._document
        d.readableid = GuiHelper.get_val(self.m_kennummerTB)
        d.documentgroup = GuiHelper.get_sqp_objval(self.m_groupCB, self._docgroups)
        if d.documentgroup is not None:
            d.groupid = d.documentgroup._id
        else:
            d.groupid = None

        d.type = GuiHelper.get_val(self.m_doctypCB, self._doctypelist)
        d.title = GuiHelper.get_val(self.m_titelTB)
        d.scandate = GuiHelper.get_val(self.m_scanDatumDP)
        d.productiondate = GuiHelper.get_val(self.m_produktionsDatumDP)
        #the follwing fields are readonly in the GUI - no update needed
        #p.filepath = GuiHelper.get_val(self.m_wxarchivepathTB)
        #p.ext = GuiHelper.get_val(self.m_docextTB)

        if d.type is None: #make sure we do not store empty types
            d.type = self._get_unspec_type()

        self._fact.flush(d)
        return res
    
    def uploadDocument(self, event):
        if self._document.filepath is not None:
            GuiHelper.show_error("Bitte entferne zuerst das bereits angehängte Dokument")

        with wx.FileDialog(self, "Dateiauswahl", wildcard="PDFs | *.pdf; | Alle Dateien | *.*",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed his mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                archname, extname = self._docarchive.archive_file(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

            self._document.filepath = archname
            self._document.ext = extname
            self._fact.flush(self._document)
            GuiHelper.set_val(self.m_archivepathTB, archname)
            GuiHelper.set_val(self.m_docextTB, extname)
            self.Refresh()


    def removeDocument(self, event):
        res = wx.MessageBox(parent=self,
                      message="Bist du sicher, dass das Dokument entfernt werden soll?",
                      caption="Rückfrage",
                      style=wx.YES_NO)
        if res == wx.ID_NO:
            return
        
        if self._document.filepath is not None and len(self._document.filepath)>0:
            self._docarchive.remove_file(self._document.filepath)
            self._document.filepath = None
            self._document.ext = None
            GuiHelper.set_val(self.m_archivepathTB, None)
            GuiHelper.set_val(self.m_docextTB, None)
            self._fact.flush(self._document) #make sure that database reflects archive state
            self.Refresh()

    def _downloadtotemp(self, pathname):
        try:
            return self._docarchive.extract_file(pathname, self._temp)
        except IOError:
            wx.LogError("Cannot open file '%s'." % pathname)


    def viewDocument(self, event):
        """download the document temporarily and view it with whatever the op-system wants to open it with"""
        if self._document.filepath is None:
            GuiHelper.show_error("Es wurde kein Dokument archiviert.")
            return

        extrpname = self._downloadtotemp(self._document.filepath)
        GuiHelper.openbysys(extrpname)

    def addInfoBit(self, event):
        newib = DocumentInfoBit(targetid = self._document._id,
                               infocontent="<Infotext hier>",
                               infodate = datetime.datetime.now())
        self._fact.flush(newib)

        self._document.docinfobits.append(newib)
        # idx = len(self._document.docinfobits)-1
        # self._add_ibline(idx, newib)
        GuiHelper.append_data_for_lstctrl(self.m_zusatzinfoLCT, self.DOCINFODEFINS, newib)

    def editInfoBit(self, event):
        selib = GuiHelper.get_selected_fromlctrl(self.m_zusatzinfoLCT, self._document.docinfobits)
        if selib is None: return

        dial =  EditInfoBitDialog(self, self._fact, selib)
        res = dial.showmodal()

        if res == wx.ID_CANCEL: return

        self._fill_ibcols()

    def removeInfoBit(self, event):
        selib = GuiHelper.get_selected_fromlctrl(self.m_zusatzinfoLCT, self.document.docinfobits)
        if selib is None: return

        res = wx.MessageBox("Soll die Information wirklich gelöscht werden?", "Rückfrage", style=wx.YES_NO, parent=self)
        if res == wx.YES:
            self._fact.delete(selib)
            
            remid = -1
            ct = 0
            for ib in self._document.docinfobits:
                if ib._id == selib._id:
                    remid = ct
                ct += 1

            if remid >= 0:
                self._document.docinfobits.pop(remid)

            self._fill_ibcols()



    def connectPerson(self, event):
        alreadyconn = []
        for connper in self._connected_persons:
            alreadyconn.append(connper.personid)

        addpidial = FindPersonsDialog(self, self._fact, alreadyconn)
        res = addpidial.showmodal()

        if res == wx.ID_CANCEL: return

        #adding one ore more person link to the current pictuere now
        for adper in addpidial.selected:
            inter = PersonDocumentInter_Hollow(documentid=self._document._id,
                                              personid=adper._id)
            self._fact.flush(inter)

        self._fill_connpersons()
        
        
    def disconnectPerson(self, event):
        selpinter = GuiHelper.get_selected_fromlctrl(self.m_conPersoLCTRL, self._connected_persons)

        if selpinter is None: return

        self._fact.delete(selpinter)
        self._fill_connpersons()
    
    def conPerSelected(self, event):
        selcon = GuiHelper.get_selected_fromlctrl(self.m_conPersoLCTRL, self._connected_persons)
        GuiHelper.enable_ctrls(selcon is not None, self.m_removePersonsBU)

    def conPerDeSelected(self, event):
        selcon = GuiHelper.get_selected_fromlctrl(self.m_conPersoLCTRL, self._connected_persons)
        GuiHelper.enable_ctrls(selcon is not None, self.m_removePersonsBU)