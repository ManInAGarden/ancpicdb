from datetime import datetime
import csv
import wx
import wx.adv
import GeneratedGUI as gg
from GuiHelper import GuiHelper
from PersistClasses import Document, DocTypeCat
import sqlitepersist as sqp
from ConfigReader import ConfigReader
from EditDocumentDialog import EditDocumentDialog
from ConnectedPersonsDialog import ConnectedPersonsDialog
from DocumentFilterData import DocumentFilterData
from DocumentFilterDialog import DocumentFilterDialog
import backgroundworkers as bgw

class DocumentsViewDialog(gg.gDocumentsViewDialog):

    DOCLISTDEFINS=[
        {"propname" : "readableid", "title": "ID", "width":230},
        {"propname" : "scandate", "title": "Scandatum", "width":100, "format": "{:%d.%m.%Y}"},
        {"propname" : "productiondate", "title": "Erstelldatum", "width":100, "format": "{:%d.%m.%Y}"},
        {"propname" : "title", "title": "Titel", "width":380},
        #{"propname" : "groupname", "title": "Gruppe", "width":250},
        {"propname" : "type.value", "title": "Typ", "width":40},
        {"propname" : "documentgroup.groupordername", "title": "Grp#", "width":60}
    ]
    @property
    def configuration(self):
        return self._configuration
    
    @property
    def docarchive(self):
        return self._docarchive

    def __init__(self, parent, fact):
        super().__init__(parent)

        GuiHelper.set_icon(self)
        self._fact = fact
        self._docarchive = parent.docarchive
        self._configuration = parent.configuration
        self.logger = parent.logger
        self.machlabel = self._configuration.get_value("gui", "machlabel")
        if self.machlabel is None:
            self.machlabel = "XXXX"
        
        self._filter = DocumentFilterData(fact) #current active filter for the data
        
        bgw.EVT_RESULT(self, self.workerfinished)
        bgw.EVT_NOTIFY_PERC(self, self.notifyperc)

    def workerfinished(self, event : bgw.ResultEvent):
        GuiHelper.enable_ctrls(True, self.m_folderUploadBU)
        self._filldialog() #refectch pictures from the db and display them in the list

    def notifyperc(self, event):
        perc = event.data
        GuiHelper.set_val(self.m_workingGAUGE, perc)


    def _prep_cols(self):
        GuiHelper.set_columns_forlstctrl(self.m_documentsLCTRL, self.DOCLISTDEFINS)
        
    def showmodal(self):
        self._prep_cols()
        self._filldialog()

        return self.ShowModal()
    
    def _filldialog(self):
        """fill dialog with all the pictures"""
        self._refilldialog()
        

    def _refilldialog(self):
        """fill dialog with all the documents filtered if filter hase been set"""
        #requery the document data
        if self._filter is not None:
            q = self._filter.get_query()
        else:
            q = sqp.SQQuery(self._fact, Document).order_by(sqp.OrderInfo(Document.ScanDate, sqp.OrderDirection.DESCENDING))

        self._documents = q.as_list()
        GuiHelper.set_data_for_lstctrl(self.m_documentsLCTRL,
                                       self.DOCLISTDEFINS,
                                       self._documents)

    def _create_readid(self):
        dt = datetime.now()
        return "{0}.{1:%Y%m%d.%H%M%S.%f}".format(self.machlabel, dt)

    def addNewRow(self, event):
        readid = self._create_readid()
        doc = Document(readableid=readid)
        doc.type = self._fact.getcat(DocTypeCat, "NSP") #initialise as unspecified
        self._fact.flush(doc)
        self._documents.append(doc)
        
        GuiHelper.append_data_for_lstctrl(self.m_documentsLCTRL,
                                          self.DOCLISTDEFINS,
                                          doc)

    def removeRow(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)

        if seldoc is None:
            return
        
        if seldoc.readableid is not None:
            name = seldoc.readableid
        elif seldoc.title is not None:
            name = seldoc.title
        else:
            name = "kein Name"

        res = wx.MessageBox("Soll das Dokument <{}> tatsächlich gelöscht werden?".format(name),
                            "Rückfrage",
                            style=wx.YES_NO)
        
        if res != wx.YES:
            return 

        self._fact.delete(seldoc)
        self.logger.WriteInfo("Row for document {} removed and document deleted", seldoc._id)

        self._filldialog()

    def _editElement(self, document):
        dial = EditDocumentDialog(self, self._fact, document)
        res = dial.showmodal()
        if res == wx.ID_CANCEL:
            return
        
        self._filldialog()

    def editButnClick(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
    
        if seldoc is None:
            return
        
        self._editElement(seldoc)


    def downloadDocument(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)

        if seldoc is None: return
        

    def documentSelected(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        
        GuiHelper.enable_ctrls(seldoc != None, 
                                   self.m_downloadDocumentBU, 
                                   self.m_editBU,
                                   self.m_deleteDocumentBU,
                                   self.m_preparePrintBU,
                                   self.m_showConnectedPersonsBU)
        
    def documentDeselected(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        
        GuiHelper.enable_ctrls(seldoc != None, 
                                   self.m_downloadDocumentBU, 
                                   self.m_editBU,
                                   self.m_deleteDocumentBU,
                                   self.m_preparePrintBU,
                                   self.m_showConnectedPersonsBU)


    def listDblClick(self, event):
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        if seldoc == None: return
        self._editElement(seldoc)


    def showConnectedPersons(self, event):
        """display and edit the connections to persons of the selected document or to the first selected document
           if more than one is selected
        """
        seldoc = GuiHelper.get_selected_fromlctrl(self.m_documentsLCTRL, self._documents)
        
        if seldoc is None: return

        conndial = ConnectedPersonsDialog(self, self._fact, seldoc)
        conndial.showmodal()

    def doFolderUpload(self, event):
        res = GuiHelper.select_files(self, 
                                     "Dokumente auswählen",
                                     style=wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

        if res == None:
            return
        
        paras = {}
        paras["fact"] = self._fact
        paras["files"] = res
        paras["logger"] = self.logger
        paras["docarchiver"] = self._docarchive
        paras["machlabel"] = self.machlabel

        self.bg = bgw.BgDocumentMassArchiving(notifywin=self, paras = paras)
        self.m_workingGAUGE.Show()

        self.bg.start()

        GuiHelper.enable_ctrls(False, self.m_folderUploadBU)

    def doPreparePrint(self, event):
        """create a list (csv) with info of the selected documents, ready to be used in a label print
        """
        seldocs = GuiHelper.get_all_selected_fromlctrl(self.m_documentsLCTRL, self._documents)

        if seldocs is None or len(seldocs)==0: return

        filename = GuiHelper.select_single_file(self, title="Datei für den Export auswählen", 
                                           wildcard="csv-Dateien (*.csv)|*.csv",
                                           style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if filename is None or len(filename)==0: return

        if filename.lower().endswith(".csv"):
            fname = filename
        else:
            fname = filename + ".csv"

        try:
            with open(fname, 'w', newline='',encoding="ansi") as csvfile:
                csvw = csv.writer(csvfile)
                csvw.writerow(["_id", "readableid", "title", "bestdatestr", "groupname", "grouponum"])
                for sd in seldocs:
                    csvw.writerow([sd._id, sd.readableid, sd.besttitle, sd.bestdatestr, sd.groupname, sd.groupordernum])
                
            GuiHelper.show_message("CSV Datei unter <{}> erfolgreich geschrieben", fname)
        except Exception as exc:
            GuiHelper.show_error("Die Datei kann nicht geschrieben werden. {}", exc)

    def applyFilter(self, event):
        edifiltdial = DocumentFilterDialog(self, self._fact, self._filter)

        res = edifiltdial.showmodal()

        if res == wx.ID_CANCEL:
            return
            
        self._filter = edifiltdial.filter
        GuiHelper.set_val(self.m_filterInfoTB, self._filter.get_info())
        self._refilldialog()