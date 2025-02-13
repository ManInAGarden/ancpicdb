# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv
import wx.html

###########################################################################
## Class AncPicDBMain
###########################################################################

class AncPicDBMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"AncPicDB", pos = wx.DefaultPosition, size = wx.Size( 1200,650 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )

		self.m_mainMenuBar = wx.MenuBar( 0 )
		self.m_fileMenu = wx.Menu()
		self.m_changeDbMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Datenbank wechseln"+ u"\t" + u"CTRL+O", u"Zu einer anderen bestehenden Datenbank wechseln", wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_changeDbMI )

		self.m_backupDbMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Sicherungskopie erstellen", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_backupDbMI )

		self.m_importSUBM = wx.Menu()
		self.m_importCsvMI = wx.MenuItem( self.m_importSUBM, wx.ID_ANY, u"CSV-Import", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_importSUBM.Append( self.m_importCsvMI )

		self.m_fileMenu.AppendSubMenu( self.m_importSUBM, u"Import" )

		self.m_export = wx.Menu()
		self.m_extractArchives = wx.MenuItem( self.m_export, wx.ID_ANY, u"Archive extrahieren", u"Extrahiert Doukmente und Bilder so, dass sie separat gespeichert werden können", wx.ITEM_NORMAL )
		self.m_export.Append( self.m_extractArchives )

		self.mexportCSV = wx.MenuItem( self.m_export, wx.ID_ANY, u"CSV-Export", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_export.Append( self.mexportCSV )

		self.m_fileMenu.AppendSubMenu( self.m_export, u"Export" )

		self.m_createNewDatabaseMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Neue Datenbank anlegen", u"Eine neue Datenbank anlegen und dabei gg. eine bestehende kopieren", wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_createNewDatabaseMI )

		self.m_fileMenu.AppendSeparator()

		self.m_exitMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Beenden"+ u"\t" + u"CTRL+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_exitMI )

		self.m_mainMenuBar.Append( self.m_fileMenu, u"Datei" )

		self.m_editMenu = wx.Menu()
		self.m_groupsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Gruppen"+ u"\t" + u"CTRL+G", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_groupsMI )

		self.m_documentsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Dokumente"+ u"\t" + u"CTRL+D", u"Dokumente sichten", wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_documentsMI )

		self.m_picsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Bilder"+ u"\t" + u"CTRL+B", u"Bilder sichten", wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_picsMI )

		self.m_mainMenuBar.Append( self.m_editMenu, u"Bearbeiten" )

		self.m_menu4 = wx.Menu()
		self.m_menuItem9 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Steckbriefe produzieren", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem9 )

		self.m_menuItem10 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Daten prüfen", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem10 )

		self.m_menu1 = wx.Menu()
		self.m_printRegisterDocMI = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Dokumente", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_printRegisterDocMI )

		self.m_printRegisterPicMI = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Bilder", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_printRegisterPicMI )

		self.m_menu4.AppendSubMenu( self.m_menu1, u"Registerblätter" )

		self.m_mainMenuBar.Append( self.m_menu4, u"Extras" )

		self.m_helpMenu = wx.Menu()
		self.m_help = wx.MenuItem( self.m_helpMenu, wx.ID_ANY, u"Hilfe", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_helpMenu.Append( self.m_help )

		self.m_aboutAncPicDB = wx.MenuItem( self.m_helpMenu, wx.ID_ANY, u"Über", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_helpMenu.Append( self.m_aboutAncPicDB )

		self.m_mainMenuBar.Append( self.m_helpMenu, u"Hilfe" )

		self.SetMenuBar( self.m_mainMenuBar )

		self.m_mainWindowSB = self.CreateStatusBar( 4, wx.STB_DEFAULT_STYLE, wx.ID_ANY )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		m_mainGBSIZER = wx.GridBagSizer( 0, 0 )
		m_mainGBSIZER.SetFlexibleDirection( wx.BOTH )
		m_mainGBSIZER.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_personsLBChoices = []
		self.m_personsLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), m_personsLBChoices, wx.LB_HSCROLL|wx.LB_NEEDED_SB )
		gbSizer3.Add( self.m_personsLB, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_personsEditButtonsSIZER = wx.BoxSizer( wx.HORIZONTAL )

		self.m_newPersonBU = wx.Button( self, wx.ID_ANY, u"*", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_newPersonBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER.Add( self.m_newPersonBU, 0, wx.ALL, 5 )

		self.m_editPersonBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editPersonBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER.Add( self.m_editPersonBU, 0, wx.ALL, 5 )

		self.m_deletePersonBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deletePersonBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER.Add( self.m_deletePersonBU, 0, wx.ALL, 5 )


		gbSizer3.Add( m_personsEditButtonsSIZER, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_TOP, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Personen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		gbSizer3.Add( self.m_staticText8, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer3.AddGrowableCol( 0 )
		gbSizer3.AddGrowableRow( 1 )

		m_mainGBSIZER.Add( gbSizer3, wx.GBPosition( 0, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.EXPAND, 5 )

		gbSizer4 = wx.GridBagSizer( 0, 0 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Bilder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		gbSizer4.Add( self.m_staticText10, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_picturesLBChoices = []
		self.m_picturesLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), m_picturesLBChoices, wx.LB_HSCROLL )
		gbSizer4.Add( self.m_picturesLB, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_personsEditButtonsSIZER1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_connectPictureBU = wx.Button( self, wx.ID_ANY, u"*", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_connectPictureBU.SetBitmap( wx.Bitmap( u"ressources/Add-Link.png", wx.BITMAP_TYPE_ANY ) )
		self.m_connectPictureBU.SetBitmapDisabled( wx.NullBitmap )
		m_personsEditButtonsSIZER1.Add( self.m_connectPictureBU, 0, wx.ALL, 5 )

		self.m_editPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editPictureBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER1.Add( self.m_editPictureBU, 0, wx.ALL, 5 )

		self.m_disconnectPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_disconnectPictureBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Link.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER1.Add( self.m_disconnectPictureBU, 0, wx.ALL, 5 )


		gbSizer4.Add( m_personsEditButtonsSIZER1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer4.AddGrowableCol( 0 )
		gbSizer4.AddGrowableRow( 1 )

		m_mainGBSIZER.Add( gbSizer4, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_documentsLBChoices = []
		self.m_documentsLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), m_documentsLBChoices, wx.LB_HSCROLL )
		gbSizer5.Add( self.m_documentsLB, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Dokumente", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		gbSizer5.Add( self.m_staticText9, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_personsEditButtonsSIZER2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_connectDocumentBU = wx.Button( self, wx.ID_ANY, u"*", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_connectDocumentBU.SetBitmap( wx.Bitmap( u"ressources/Add-Link.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER2.Add( self.m_connectDocumentBU, 0, wx.ALL, 5 )

		self.m_editDocumentBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editDocumentBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER2.Add( self.m_editDocumentBU, 0, wx.ALL, 5 )

		self.m_disconnectDocumentBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_disconnectDocumentBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Link.png", wx.BITMAP_TYPE_ANY ) )
		m_personsEditButtonsSIZER2.Add( self.m_disconnectDocumentBU, 0, wx.ALL, 5 )


		gbSizer5.Add( m_personsEditButtonsSIZER2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer5.AddGrowableCol( 0 )
		gbSizer5.AddGrowableRow( 1 )

		m_mainGBSIZER.Add( gbSizer5, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		m_mainGBSIZER.AddGrowableCol( 0 )
		m_mainGBSIZER.AddGrowableCol( 1 )
		m_mainGBSIZER.AddGrowableRow( 0 )
		m_mainGBSIZER.AddGrowableRow( 1 )

		bSizer15.Add( m_mainGBSIZER, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer15 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.changeDb, id = self.m_changeDbMI.GetId() )
		self.Bind( wx.EVT_MENU, self.backupDb, id = self.m_backupDbMI.GetId() )
		self.Bind( wx.EVT_MENU, self.importCsv, id = self.m_importCsvMI.GetId() )
		self.Bind( wx.EVT_MENU, self.extractArchive, id = self.m_extractArchives.GetId() )
		self.Bind( wx.EVT_MENU, self.exportDataToCSV, id = self.mexportCSV.GetId() )
		self.Bind( wx.EVT_MENU, self.createNewDb, id = self.m_createNewDatabaseMI.GetId() )
		self.Bind( wx.EVT_MENU, self.quit, id = self.m_exitMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewGroupsDialog, id = self.m_groupsMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewDocumentsDialog, id = self.m_documentsMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewPicturesDialog, id = self.m_picsMI.GetId() )
		self.Bind( wx.EVT_MENU, self.printWantedPosters, id = self.m_menuItem9.GetId() )
		self.Bind( wx.EVT_MENU, self.doDataCheck, id = self.m_menuItem10.GetId() )
		self.Bind( wx.EVT_MENU, self.printDocRegister, id = self.m_printRegisterDocMI.GetId() )
		self.Bind( wx.EVT_MENU, self.printPicRegister, id = self.m_printRegisterPicMI.GetId() )
		self.Bind( wx.EVT_MENU, self.showAbout, id = self.m_aboutAncPicDB.GetId() )
		self.m_personsLB.Bind( wx.EVT_LISTBOX, self.personSelected )
		self.m_personsLB.Bind( wx.EVT_LISTBOX_DCLICK, self.editExistingPerson )
		self.m_newPersonBU.Bind( wx.EVT_LEFT_DOWN, self.editNewPerson )
		self.m_editPersonBU.Bind( wx.EVT_BUTTON, self.editExistingPerson )
		self.m_deletePersonBU.Bind( wx.EVT_LEFT_DOWN, self.deletePerson )
		self.m_picturesLB.Bind( wx.EVT_LISTBOX_DCLICK, self.editPersonsPicture )
		self.m_connectPictureBU.Bind( wx.EVT_BUTTON, self.addPicture )
		self.m_editPictureBU.Bind( wx.EVT_BUTTON, self.editPersonsPicture )
		self.m_disconnectPictureBU.Bind( wx.EVT_BUTTON, self.removePictureFromPerson )
		self.m_disconnectPictureBU.Bind( wx.EVT_LEFT_DOWN, self.disconnectPicture )
		self.m_documentsLB.Bind( wx.EVT_LISTBOX_DCLICK, self.editPersonsDocument )
		self.m_connectDocumentBU.Bind( wx.EVT_BUTTON, self.addDocument )
		self.m_editDocumentBU.Bind( wx.EVT_BUTTON, self.editPersonsDocument )
		self.m_disconnectDocumentBU.Bind( wx.EVT_BUTTON, self.removeDoumentFromPerson )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def changeDb( self, event ):
		event.Skip()

	def backupDb( self, event ):
		event.Skip()

	def importCsv( self, event ):
		event.Skip()

	def extractArchive( self, event ):
		event.Skip()

	def exportDataToCSV( self, event ):
		event.Skip()

	def createNewDb( self, event ):
		event.Skip()

	def quit( self, event ):
		event.Skip()

	def openViewGroupsDialog( self, event ):
		event.Skip()

	def openViewDocumentsDialog( self, event ):
		event.Skip()

	def openViewPicturesDialog( self, event ):
		event.Skip()

	def printWantedPosters( self, event ):
		event.Skip()

	def doDataCheck( self, event ):
		event.Skip()

	def printDocRegister( self, event ):
		event.Skip()

	def printPicRegister( self, event ):
		event.Skip()

	def showAbout( self, event ):
		event.Skip()

	def personSelected( self, event ):
		event.Skip()

	def editExistingPerson( self, event ):
		event.Skip()

	def editNewPerson( self, event ):
		event.Skip()


	def deletePerson( self, event ):
		event.Skip()

	def editPersonsPicture( self, event ):
		event.Skip()

	def addPicture( self, event ):
		event.Skip()


	def removePictureFromPerson( self, event ):
		event.Skip()

	def disconnectPicture( self, event ):
		event.Skip()

	def editPersonsDocument( self, event ):
		event.Skip()

	def addDocument( self, event ):
		event.Skip()


	def removeDoumentFromPerson( self, event ):
		event.Skip()


###########################################################################
## Class geditDocumentDialog
###########################################################################

class geditDocumentDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dokument bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 860,760 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer7 = wx.GridBagSizer( 0, 0 )
		gbSizer7.SetFlexibleDirection( wx.BOTH )
		gbSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize()

		gbSizer7.Add( m_sdbSizer3, wx.GBPosition( 10, 3 ), wx.GBSpan( 1, 3 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Kennummer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		gbSizer7.Add( self.m_staticText13, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennummerTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.m_kennummerTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText67 = wx.StaticText( self, wx.ID_ANY, u"Dokumentgruppe:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText67.Wrap( -1 )

		gbSizer7.Add( self.m_staticText67, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_groupCBChoices = []
		self.m_groupCB = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), m_groupCBChoices, wx.CB_READONLY )
		gbSizer7.Add( self.m_groupCB, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Typ:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		gbSizer7.Add( self.m_staticText14, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_doctypCBChoices = []
		self.m_doctypCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_doctypCBChoices, wx.CB_READONLY )
		gbSizer7.Add( self.m_doctypCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText30 = wx.StaticText( self, wx.ID_ANY, u"Titel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )

		gbSizer7.Add( self.m_staticText30, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titelTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.m_titelTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"Produktionsdatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		gbSizer7.Add( self.m_staticText15, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_produktionsDatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer7.Add( self.m_produktionsDatumDP, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText88 = wx.StaticText( self, wx.ID_ANY, u"Personenbezüge:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText88.Wrap( -1 )

		gbSizer7.Add( self.m_staticText88, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Scandatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		gbSizer7.Add( self.m_staticText16, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Informationen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gbSizer7.Add( self.m_staticText18, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_zusatzinfoLCT = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer7.Add( self.m_zusatzinfoLCT, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addPictBitInfoBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addPictBitInfoBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer5.Add( self.m_addPictBitInfoBU, 0, wx.ALL, 5 )

		self.m_editPictBitInfoBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editPictBitInfoBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer5.Add( self.m_editPictBitInfoBU, 0, wx.ALL, 5 )

		self.m_deletePictBitInfoBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deletePictBitInfoBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer5.Add( self.m_deletePictBitInfoBU, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer5, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_TOP|wx.EXPAND, 5 )

		self.m_scanDatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer7.Add( self.m_scanDatumDP, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_conPersoLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer7.Add( self.m_conPersoLCTRL, wx.GBPosition( 4, 4 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText181 = wx.StaticText( self, wx.ID_ANY, u"Archivdatei:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181.Wrap( -1 )

		gbSizer7.Add( self.m_staticText181, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_archivepathTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_BESTWRAP|wx.TE_READONLY )
		gbSizer7.Add( self.m_archivepathTB, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_docextTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer7.Add( self.m_docextTB, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText87 = wx.StaticText( self, wx.ID_ANY, u"Archivierter Typ:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText87.Wrap( -1 )

		gbSizer7.Add( self.m_staticText87, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_uploadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_uploadBU.SetBitmap( wx.Bitmap( u"ressources/Upload.png", wx.BITMAP_TYPE_ANY ) )
		self.m_uploadBU.SetToolTip( u"Ein Bild von der lokalen Festplatte hochladen" )

		bSizer6.Add( self.m_uploadBU, 0, wx.ALL, 5 )

		self.m_viewDocumentBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_viewDocumentBU.SetBitmap( wx.Bitmap( u"ressources/Visible-32.png", wx.BITMAP_TYPE_ANY ) )
		bSizer6.Add( self.m_viewDocumentBU, 0, wx.ALL, 5 )

		self.m_downloadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_downloadBU.SetBitmap( wx.Bitmap( u"ressources/Download.png", wx.BITMAP_TYPE_ANY ) )
		self.m_downloadBU.SetToolTip( u"Das Bild auf die lokale Festplatte hereunterladen" )

		bSizer6.Add( self.m_downloadBU, 0, wx.ALL, 5 )

		self.m_button23 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_button23.SetBitmap( wx.Bitmap( u"ressources/Remove-Image.png", wx.BITMAP_TYPE_ANY ) )
		self.m_button23.SetToolTip( u"Den Bildinhalt entfernen" )

		bSizer6.Add( self.m_button23, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer6, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addPersonsBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addPersonsBU.SetBitmap( wx.Bitmap( u"ressources/Add-Link.png", wx.BITMAP_TYPE_ANY ) )
		bSizer26.Add( self.m_addPersonsBU, 0, wx.ALL, 5 )

		self.m_removePersonsBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removePersonsBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Link.png", wx.BITMAP_TYPE_ANY ) )
		self.m_removePersonsBU.Enable( False )

		bSizer26.Add( self.m_removePersonsBU, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer26, wx.GBPosition( 7, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer7.AddGrowableCol( 1 )
		gbSizer7.AddGrowableRow( 8 )

		self.SetSizer( gbSizer7 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_zusatzinfoLCT.Bind( wx.EVT_LEFT_DCLICK, self.editInfoBit )
		self.m_addPictBitInfoBU.Bind( wx.EVT_BUTTON, self.addInfoBit )
		self.m_editPictBitInfoBU.Bind( wx.EVT_BUTTON, self.editInfoBit )
		self.m_deletePictBitInfoBU.Bind( wx.EVT_BUTTON, self.removeInfoBit )
		self.m_conPersoLCTRL.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.conPerDeSelected )
		self.m_conPersoLCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.conPerSelected )
		self.m_uploadBU.Bind( wx.EVT_BUTTON, self.uploadDocument )
		self.m_viewDocumentBU.Bind( wx.EVT_BUTTON, self.viewDocument )
		self.m_downloadBU.Bind( wx.EVT_BUTTON, self.downloadDocument )
		self.m_button23.Bind( wx.EVT_BUTTON, self.removeDocument )
		self.m_addPersonsBU.Bind( wx.EVT_BUTTON, self.connectPerson )
		self.m_removePersonsBU.Bind( wx.EVT_BUTTON, self.disconnectPerson )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def editInfoBit( self, event ):
		event.Skip()

	def addInfoBit( self, event ):
		event.Skip()


	def removeInfoBit( self, event ):
		event.Skip()

	def conPerDeSelected( self, event ):
		event.Skip()

	def conPerSelected( self, event ):
		event.Skip()

	def uploadDocument( self, event ):
		event.Skip()

	def viewDocument( self, event ):
		event.Skip()

	def downloadDocument( self, event ):
		event.Skip()

	def removeDocument( self, event ):
		event.Skip()

	def connectPerson( self, event ):
		event.Skip()

	def disconnectPerson( self, event ):
		event.Skip()


###########################################################################
## Class gDocumentsViewDialog
###########################################################################

class gDocumentsViewDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dokumente sichten", pos = wx.DefaultPosition, size = wx.Size( 966,567 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_documentsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer6.Add( self.m_documentsLCTRL, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText99 = wx.StaticText( self, wx.ID_ANY, u"Filter:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText99.Wrap( -1 )

		gbSizer6.Add( self.m_staticText99, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_filterInfoTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer6.Add( self.m_filterInfoTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_ApplyFilterBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_ApplyFilterBU.SetBitmap( wx.Bitmap( u"ressources/Filled-Filter.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_ApplyFilterBU, 0, wx.ALL, 5 )

		self.m_addRowBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addRowBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_addRowBU, 0, wx.ALL, 5 )

		self.m_editBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		self.m_editBU.Enable( False )

		bSizer10.Add( self.m_editBU, 0, wx.ALL, 5 )

		self.m_downloadDocumentBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_downloadDocumentBU.SetBitmap( wx.Bitmap( u"ressources/Download.png", wx.BITMAP_TYPE_ANY ) )
		self.m_downloadDocumentBU.Enable( False )

		bSizer10.Add( self.m_downloadDocumentBU, 0, wx.ALL, 5 )

		self.m_deleteDocumentBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deleteDocumentBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		self.m_deleteDocumentBU.Enable( False )

		bSizer10.Add( self.m_deleteDocumentBU, 0, wx.ALL, 5 )

		self.m_showConnectedPersonsBU = wx.Button( self, wx.ID_ANY, u"Personen", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_showConnectedPersonsBU.SetBitmap( wx.Bitmap( u"ressources/icons8-connected-30.png", wx.BITMAP_TYPE_ANY ) )
		self.m_showConnectedPersonsBU.Enable( False )
		self.m_showConnectedPersonsBU.SetToolTip( u"Verbundene Personen anzeigen" )

		bSizer10.Add( self.m_showConnectedPersonsBU, 0, wx.ALL, 5 )

		self.m_folderUploadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_folderUploadBU.SetBitmap( wx.Bitmap( u"ressources/FolderUpload.png", wx.BITMAP_TYPE_ANY ) )
		self.m_folderUploadBU.SetToolTip( u"Bildeinträge aus Bilddateien anlegen" )

		bSizer10.Add( self.m_folderUploadBU, 0, wx.ALL, 5 )

		self.m_preparePrintBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_preparePrintBU.SetBitmap( wx.Bitmap( u"ressources/icons8-print-32.png", wx.BITMAP_TYPE_ANY ) )
		self.m_preparePrintBU.Enable( False )

		bSizer10.Add( self.m_preparePrintBU, 0, wx.ALL, 5 )

		self.m_workingGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_workingGAUGE.SetValue( 0 )
		self.m_workingGAUGE.Hide()
		self.m_workingGAUGE.SetToolTip( u"Fortschritt der Hintergrundaufgabe" )

		bSizer10.Add( self.m_workingGAUGE, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		gbSizer6.Add( bSizer10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Dokumente:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer6.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		m_sdbSizer2.Realize()

		gbSizer6.Add( m_sdbSizer2, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 1 )
		gbSizer6.AddGrowableRow( 1 )

		self.SetSizer( gbSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_documentsLCTRL.Bind( wx.EVT_LEFT_DCLICK, self.listDblClick )
		self.m_documentsLCTRL.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.documentDeselected )
		self.m_documentsLCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.documentSelected )
		self.m_ApplyFilterBU.Bind( wx.EVT_BUTTON, self.applyFilter )
		self.m_addRowBU.Bind( wx.EVT_BUTTON, self.addNewRow )
		self.m_editBU.Bind( wx.EVT_BUTTON, self.editButnClick )
		self.m_downloadDocumentBU.Bind( wx.EVT_BUTTON, self.downloadDocument )
		self.m_deleteDocumentBU.Bind( wx.EVT_BUTTON, self.removeRow )
		self.m_showConnectedPersonsBU.Bind( wx.EVT_BUTTON, self.showConnectedPersons )
		self.m_folderUploadBU.Bind( wx.EVT_BUTTON, self.doFolderUpload )
		self.m_preparePrintBU.Bind( wx.EVT_BUTTON, self.doPreparePrint )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def listDblClick( self, event ):
		event.Skip()

	def documentDeselected( self, event ):
		event.Skip()

	def documentSelected( self, event ):
		event.Skip()

	def applyFilter( self, event ):
		event.Skip()

	def addNewRow( self, event ):
		event.Skip()

	def editButnClick( self, event ):
		event.Skip()

	def downloadDocument( self, event ):
		event.Skip()

	def removeRow( self, event ):
		event.Skip()

	def showConnectedPersons( self, event ):
		event.Skip()

	def doFolderUpload( self, event ):
		event.Skip()

	def doPreparePrint( self, event ):
		event.Skip()


###########################################################################
## Class geditPictureDialog
###########################################################################

class geditPictureDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bild bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 800,760 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer7 = wx.GridBagSizer( 0, 0 )
		gbSizer7.SetFlexibleDirection( wx.BOTH )
		gbSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize()

		gbSizer7.Add( m_sdbSizer3, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 4 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Kennummer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		gbSizer7.Add( self.m_staticText13, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennummerTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.m_kennummerTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"Bildgruppe:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )

		gbSizer7.Add( self.m_staticText42, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_groupCBChoices = []
		self.m_groupCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_groupCBChoices, 0 )
		gbSizer7.Add( self.m_groupCB, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Titel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		gbSizer7.Add( self.m_staticText14, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titelTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.m_titelTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"Aufnahmedatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		gbSizer7.Add( self.m_staticText15, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_aufnahmeDatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer7.Add( self.m_aufnahmeDatumDP, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText43 = wx.StaticText( self, wx.ID_ANY, u"oder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )

		gbSizer7.Add( self.m_staticText43, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		m_fluffytakenmonthCBChoices = []
		self.m_fluffytakenmonthCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_fluffytakenmonthCBChoices, 0 )
		bSizer11.Add( self.m_fluffytakenmonthCB, 0, wx.ALL, 5 )

		self.m_fluffytakenyearSPCTRL = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 2100, 0 )
		bSizer11.Add( self.m_fluffytakenyearSPCTRL, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer11, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Scandatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		gbSizer7.Add( self.m_staticText16, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Beschreibung:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		gbSizer7.Add( self.m_staticText17, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_beschreibungTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RICH2 )
		gbSizer7.Add( self.m_beschreibungTB, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Informationen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gbSizer7.Add( self.m_staticText18, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_zusatzinfoLCT = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer7.Add( self.m_zusatzinfoLCT, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addPictBitInfoBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addPictBitInfoBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer5.Add( self.m_addPictBitInfoBU, 0, wx.ALL, 5 )

		self.m_editPictBitInfoBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editPictBitInfoBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer5.Add( self.m_editPictBitInfoBU, 0, wx.ALL, 5 )

		self.m_deletePictBitInfoBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deletePictBitInfoBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer5.Add( self.m_deletePictBitInfoBU, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer5, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_TOP|wx.EXPAND, 5 )

		self.m_scanDatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer7.Add( self.m_scanDatumDP, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText181 = wx.StaticText( self, wx.ID_ANY, u"Bildinhalt:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181.Wrap( -1 )

		gbSizer7.Add( self.m_staticText181, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_bitmapPAN = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer7.Add( self.m_bitmapPAN, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_persoOnPicLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer7.Add( self.m_persoOnPicLCTRL, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_connectPersonBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_connectPersonBU.SetBitmap( wx.Bitmap( u"ressources/Add-Link.png", wx.BITMAP_TYPE_ANY ) )
		bSizer25.Add( self.m_connectPersonBU, 0, wx.ALL, 5 )

		self.m_disconnectPersonBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_disconnectPersonBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Link.png", wx.BITMAP_TYPE_ANY ) )
		self.m_disconnectPersonBU.Enable( False )

		bSizer25.Add( self.m_disconnectPersonBU, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer25, wx.GBPosition( 5, 3 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_uploadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_uploadBU.SetBitmap( wx.Bitmap( u"ressources/Upload.png", wx.BITMAP_TYPE_ANY ) )
		self.m_uploadBU.SetToolTip( u"Ein Bild von der lokalen Festplatte hochladen" )

		bSizer6.Add( self.m_uploadBU, 0, wx.ALL, 5 )

		self.m_viewBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_viewBU.SetBitmap( wx.Bitmap( u"ressources/Visible-32.png", wx.BITMAP_TYPE_ANY ) )
		bSizer6.Add( self.m_viewBU, 0, wx.ALL, 5 )

		self.m_downloadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_downloadBU.SetBitmap( wx.Bitmap( u"ressources/Download.png", wx.BITMAP_TYPE_ANY ) )
		self.m_downloadBU.SetToolTip( u"Das Bild auf die lokale Festplatte hereunterladen" )

		bSizer6.Add( self.m_downloadBU, 0, wx.ALL, 5 )

		self.m_button23 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_button23.SetBitmap( wx.Bitmap( u"ressources/Remove-Image.png", wx.BITMAP_TYPE_ANY ) )
		self.m_button23.SetToolTip( u"Den Bildinhalt entfernen" )

		bSizer6.Add( self.m_button23, 0, wx.ALL, 5 )


		gbSizer7.Add( bSizer6, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer7.AddGrowableCol( 1 )
		gbSizer7.AddGrowableCol( 3 )
		gbSizer7.AddGrowableRow( 4 )
		gbSizer7.AddGrowableRow( 6 )
		gbSizer7.AddGrowableRow( 7 )
		gbSizer7.AddGrowableRow( 9 )

		self.SetSizer( gbSizer7 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_zusatzinfoLCT.Bind( wx.EVT_LEFT_DCLICK, self.editInfoBit )
		self.m_addPictBitInfoBU.Bind( wx.EVT_BUTTON, self.addInfoBit )
		self.m_editPictBitInfoBU.Bind( wx.EVT_BUTTON, self.editInfoBit )
		self.m_deletePictBitInfoBU.Bind( wx.EVT_BUTTON, self.removeInfoBit )
		self.m_persoOnPicLCTRL.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.personDeselected )
		self.m_persoOnPicLCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.personSelected )
		self.m_connectPersonBU.Bind( wx.EVT_BUTTON, self.addPerson )
		self.m_disconnectPersonBU.Bind( wx.EVT_BUTTON, self.removePerson )
		self.m_uploadBU.Bind( wx.EVT_BUTTON, self.uploadPicture )
		self.m_viewBU.Bind( wx.EVT_BUTTON, self.viewPicture )
		self.m_downloadBU.Bind( wx.EVT_BUTTON, self.downloadPicture )
		self.m_button23.Bind( wx.EVT_BUTTON, self.removePicture )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def editInfoBit( self, event ):
		event.Skip()

	def addInfoBit( self, event ):
		event.Skip()


	def removeInfoBit( self, event ):
		event.Skip()

	def personDeselected( self, event ):
		event.Skip()

	def personSelected( self, event ):
		event.Skip()

	def addPerson( self, event ):
		event.Skip()

	def removePerson( self, event ):
		event.Skip()

	def uploadPicture( self, event ):
		event.Skip()

	def viewPicture( self, event ):
		event.Skip()

	def downloadPicture( self, event ):
		event.Skip()

	def removePicture( self, event ):
		event.Skip()


###########################################################################
## Class gPicturesViewDialog
###########################################################################

class gPicturesViewDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bilder sichten", pos = wx.DefaultPosition, size = wx.Size( 1002,590 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Bilder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer6.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_picturesLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer6.Add( self.m_picturesLCTRL, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_applyFilterBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_applyFilterBU.SetBitmap( wx.Bitmap( u"ressources/Filled-Filter.png", wx.BITMAP_TYPE_ANY ) )
		self.m_applyFilterBU.SetToolTip( u"Filter für Bilderliste bearbeiten" )

		bSizer10.Add( self.m_applyFilterBU, 0, wx.ALL, 5 )

		self.m_addPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addPictureBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		self.m_addPictureBU.SetToolTip( u"Neuen Bildeintrag hinzufügen" )

		bSizer10.Add( self.m_addPictureBU, 0, wx.ALL, 5 )

		self.m_editBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		self.m_editBU.Enable( False )
		self.m_editBU.SetToolTip( u"Den markierten Bildeintrag bearbeiten" )

		bSizer10.Add( self.m_editBU, 0, wx.ALL, 5 )

		self.m_downloadPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_downloadPictureBU.SetBitmap( wx.Bitmap( u"ressources/Download.png", wx.BITMAP_TYPE_ANY ) )
		self.m_downloadPictureBU.Enable( False )
		self.m_downloadPictureBU.SetToolTip( u"Das Bild aus dem Bildeintrag herunterladen" )

		bSizer10.Add( self.m_downloadPictureBU, 0, wx.ALL, 5 )

		self.m_deletePictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deletePictureBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		self.m_deletePictureBU.Enable( False )
		self.m_deletePictureBU.SetToolTip( u"Den markierten Bildeintrag und das archivierte Bild löschen" )

		bSizer10.Add( self.m_deletePictureBU, 0, wx.ALL, 5 )

		self.m_showConnectedPersonsBU = wx.Button( self, wx.ID_ANY, u"Personen", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_showConnectedPersonsBU.SetBitmap( wx.Bitmap( u"ressources/icons8-connected-30.png", wx.BITMAP_TYPE_ANY ) )
		self.m_showConnectedPersonsBU.Enable( False )
		self.m_showConnectedPersonsBU.SetToolTip( u"Verbundene Personen anzeigen" )

		bSizer10.Add( self.m_showConnectedPersonsBU, 0, wx.ALL, 5 )

		self.m_folderUploadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_folderUploadBU.SetBitmap( wx.Bitmap( u"ressources/FolderUpload.png", wx.BITMAP_TYPE_ANY ) )
		self.m_folderUploadBU.SetToolTip( u"Bildeinträge aus Bilddateien anlegen" )

		bSizer10.Add( self.m_folderUploadBU, 0, wx.ALL, 5 )

		self.m_preparePrintBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_preparePrintBU.SetBitmap( wx.Bitmap( u"ressources/icons8-print-32.png", wx.BITMAP_TYPE_ANY ) )
		self.m_preparePrintBU.Enable( False )

		bSizer10.Add( self.m_preparePrintBU, 0, wx.ALL, 5 )

		self.m_workingGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_workingGAUGE.SetValue( 0 )
		self.m_workingGAUGE.Hide()
		self.m_workingGAUGE.SetToolTip( u"Fortschritt der Hintergrundaufgabe" )

		bSizer10.Add( self.m_workingGAUGE, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )


		gbSizer6.Add( bSizer10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		m_sdbSizer2.Realize()

		gbSizer6.Add( m_sdbSizer2, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText49 = wx.StaticText( self, wx.ID_ANY, u"Filter:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )

		gbSizer6.Add( self.m_staticText49, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_filterInfoTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer6.Add( self.m_filterInfoTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 1 )
		gbSizer6.AddGrowableRow( 1 )

		bSizer16.Add( gbSizer6, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_picturesLCTRL.Bind( wx.EVT_LEFT_DCLICK, self.listDblClick )
		self.m_picturesLCTRL.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.pictureDeselected )
		self.m_picturesLCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.pictureSelected )
		self.m_applyFilterBU.Bind( wx.EVT_BUTTON, self.applyFilter )
		self.m_addPictureBU.Bind( wx.EVT_BUTTON, self.addNewPicture )
		self.m_editBU.Bind( wx.EVT_BUTTON, self.editPicture )
		self.m_downloadPictureBU.Bind( wx.EVT_BUTTON, self.downloadPicture )
		self.m_deletePictureBU.Bind( wx.EVT_BUTTON, self.removePicture )
		self.m_showConnectedPersonsBU.Bind( wx.EVT_BUTTON, self.showConnectedPersons )
		self.m_folderUploadBU.Bind( wx.EVT_BUTTON, self.doFolderUpload )
		self.m_preparePrintBU.Bind( wx.EVT_BUTTON, self.doPreparePrint )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def listDblClick( self, event ):
		event.Skip()

	def pictureDeselected( self, event ):
		event.Skip()

	def pictureSelected( self, event ):
		event.Skip()

	def applyFilter( self, event ):
		event.Skip()

	def addNewPicture( self, event ):
		event.Skip()

	def editPicture( self, event ):
		event.Skip()

	def downloadPicture( self, event ):
		event.Skip()

	def removePicture( self, event ):
		event.Skip()

	def showConnectedPersons( self, event ):
		event.Skip()

	def doFolderUpload( self, event ):
		event.Skip()

	def doPreparePrint( self, event ):
		event.Skip()


###########################################################################
## Class gPersonEditDialog
###########################################################################

class gPersonEditDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Person bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 1000,750 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Vorname/genannt:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		gbSizer2.Add( self.m_staticText8, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		gbSizer2.Add( self.m_staticText9, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_vornameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_vornameTB.SetToolTip( u"Amtlicher Vorname der Person" )

		gbSizer2.Add( self.m_vornameTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_rufnameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_rufnameTB.SetToolTip( u"Rufname der Person" )

		gbSizer2.Add( self.m_rufnameTB, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_NameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_NameTB.SetToolTip( u"Familienname der Person" )

		gbSizer2.Add( self.m_NameTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Geburtsname:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		gbSizer2.Add( self.m_staticText10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_geburtsnameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_geburtsnameTB.SetToolTip( u"Geburtsname (Familienname) der Person wenn diese ihren Namen geändert hat (z.B. durch Heirat)" )

		gbSizer2.Add( self.m_geburtsnameTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Geboren am:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer2.Add( self.m_staticText11, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_geburtsdatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer2.Add( self.m_geburtsdatumDP, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText49 = wx.StaticText( self, wx.ID_ANY, u"oder unscharfes Geburtsdatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )

		gbSizer2.Add( self.m_staticText49, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		m_fluffyMonthCBChoices = []
		self.m_fluffyMonthCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_fluffyMonthCBChoices, 0 )
		gbSizer2.Add( self.m_fluffyMonthCB, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_fluffyYearSPC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 2100, 0 )
		gbSizer2.Add( self.m_fluffyYearSPC, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Verstorben am:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		gbSizer2.Add( self.m_staticText6, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_todesdatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer2.Add( self.m_todesdatumDP, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText50 = wx.StaticText( self, wx.ID_ANY, u"oder unscharfes Todesdatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText50.Wrap( -1 )

		gbSizer2.Add( self.m_staticText50, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		m_fluffyDeathMonthCBChoices = []
		self.m_fluffyDeathMonthCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_fluffyDeathMonthCBChoices, 0 )
		gbSizer2.Add( self.m_fluffyDeathMonthCB, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_fluffyDeathYearSPC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 2100, 0 )
		gbSizer2.Add( self.m_fluffyDeathYearSPC, wx.GBPosition( 4, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_infotextTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_BESTWRAP|wx.TE_MULTILINE )
		self.m_infotextTB.SetMinSize( wx.Size( -1,100 ) )
		self.m_infotextTB.SetMaxSize( wx.Size( 400,300 ) )

		gbSizer2.Add( self.m_infotextTB, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Mutter/Vater:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		gbSizer2.Add( self.m_staticText7, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		gbSizer19 = wx.GridBagSizer( 0, 0 )
		gbSizer19.SetFlexibleDirection( wx.BOTH )
		gbSizer19.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_motherCBChoices = []
		self.m_motherCB = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_motherCBChoices, wx.CB_READONLY )
		self.m_motherCB.SetSelection( 0 )
		gbSizer19.Add( self.m_motherCB, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_removeMotherBUT = wx.Button( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		gbSizer19.Add( self.m_removeMotherBUT, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer19.AddGrowableCol( 0 )

		gbSizer2.Add( gbSizer19, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )

		gbSizer20 = wx.GridBagSizer( 0, 0 )
		gbSizer20.SetFlexibleDirection( wx.BOTH )
		gbSizer20.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_fatherCBChoices = []
		self.m_fatherCB = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_fatherCBChoices, wx.CB_READONLY )
		gbSizer20.Add( self.m_fatherCB, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_removeFatherBUT = wx.Button( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		gbSizer20.Add( self.m_removeFatherBUT, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer20.AddGrowableCol( 0 )

		gbSizer2.Add( gbSizer20, wx.GBPosition( 5, 3 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )

		m_personSDBSI = wx.StdDialogButtonSizer()
		self.m_personSDBSIOK = wx.Button( self, wx.ID_OK )
		m_personSDBSI.AddButton( self.m_personSDBSIOK )
		self.m_personSDBSICancel = wx.Button( self, wx.ID_CANCEL )
		m_personSDBSI.AddButton( self.m_personSDBSICancel )
		m_personSDBSI.Realize()

		gbSizer2.Add( m_personSDBSI, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Signifikante Bilder:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		gbSizer2.Add( self.m_staticText51, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_significantPictursLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer2.Add( self.m_significantPictursLCTRL, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_addSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_addSignPicBU, 0, wx.ALL, 5 )

		self.m_editSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_editSignPicBU, 0, wx.ALL, 5 )

		self.m_viewSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_viewSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Visible-32.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_viewSignPicBU, 0, wx.ALL, 5 )

		self.m_removeSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removeSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_removeSignPicBU, 0, wx.ALL, 5 )


		gbSizer2.Add( bSizer12, wx.GBPosition( 8, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Infotext:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		gbSizer2.Add( self.m_staticText12, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"Partner und Kinder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )

		gbSizer2.Add( self.m_staticText62, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_partners_childrenTCTRL = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		gbSizer2.Add( self.m_partners_childrenTCTRL, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )

		m_bioSexCBChoices = []
		self.m_bioSexCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_bioSexCBChoices, wx.CB_READONLY )
		gbSizer2.Add( self.m_bioSexCB, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )


		gbSizer2.AddGrowableCol( 1 )
		gbSizer2.AddGrowableCol( 2 )
		gbSizer2.AddGrowableCol( 3 )
		gbSizer2.AddGrowableCol( 4 )
		gbSizer2.AddGrowableRow( 6 )
		gbSizer2.AddGrowableRow( 7 )

		self.SetSizer( gbSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_geburtsdatumDP.Bind( wx.adv.EVT_DATE_CHANGED, self.birthDateChanged )
		self.m_todesdatumDP.Bind( wx.adv.EVT_DATE_CHANGED, self.deathDateChanged )
		self.m_removeMotherBUT.Bind( wx.EVT_BUTTON, self.removeMotherLink )
		self.m_removeFatherBUT.Bind( wx.EVT_BUTTON, self.removeFatherLink )
		self.m_significantPictursLCTRL.Bind( wx.EVT_LEFT_DCLICK, self.editPictureInfo )
		self.m_addSignPicBU.Bind( wx.EVT_BUTTON, self.addPicture )
		self.m_editSignPicBU.Bind( wx.EVT_BUTTON, self.editPictureInfo )
		self.m_viewSignPicBU.Bind( wx.EVT_BUTTON, self.viewPicture )
		self.m_removeSignPicBU.Bind( wx.EVT_BUTTON, self.removePicture )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def birthDateChanged( self, event ):
		event.Skip()

	def deathDateChanged( self, event ):
		event.Skip()

	def removeMotherLink( self, event ):
		event.Skip()

	def removeFatherLink( self, event ):
		event.Skip()

	def editPictureInfo( self, event ):
		event.Skip()

	def addPicture( self, event ):
		event.Skip()


	def viewPicture( self, event ):
		event.Skip()

	def removePicture( self, event ):
		event.Skip()


###########################################################################
## Class gAddPictureDialog
###########################################################################

class gAddPictureDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bildauswahl", pos = wx.DefaultPosition, size = wx.Size( 487,455 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer8 = wx.GridBagSizer( 0, 0 )
		gbSizer8.SetFlexibleDirection( wx.BOTH )
		gbSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize()

		gbSizer8.Add( m_sdbSizer4, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_picturesLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer8.Add( self.m_picturesLCTRL, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Titel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		gbSizer8.Add( self.m_staticText19, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titleTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.m_titleTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_button21 = wx.Button( self, wx.ID_ANY, u"Filter anwenden", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.m_button21, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Aufnamedatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		gbSizer8.Add( self.m_staticText20, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_operatorTakenCBChoices = [ u"=", u">", u"<" ]
		self.m_operatorTakenCB = wx.ComboBox( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, m_operatorTakenCBChoices, 0 )
		gbSizer8.Add( self.m_operatorTakenCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_dateTakenDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer8.Add( self.m_dateTakenDP, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Scandatum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		gbSizer8.Add( self.m_staticText21, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_operatorScannedCBChoices = [ u"=", u">", u"<" ]
		self.m_operatorScannedCB = wx.ComboBox( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, m_operatorScannedCBChoices, 0 )
		gbSizer8.Add( self.m_operatorScannedCB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_scanDateDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer8.Add( self.m_scanDateDP, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"Kennung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		gbSizer8.Add( self.m_staticText22, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennungTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.m_kennungTB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer8.AddGrowableCol( 2 )
		gbSizer8.AddGrowableRow( 6 )

		self.SetSizer( gbSizer8 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button21.Bind( wx.EVT_BUTTON, self.applyFilter )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def applyFilter( self, event ):
		event.Skip()


###########################################################################
## Class gAddDocumentDialog
###########################################################################

class gAddDocumentDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dokumentauswahl", pos = wx.DefaultPosition, size = wx.Size( 646,561 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer8 = wx.GridBagSizer( 0, 0 )
		gbSizer8.SetFlexibleDirection( wx.BOTH )
		gbSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize()

		gbSizer8.Add( m_sdbSizer4, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_documentsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer8.Add( self.m_documentsLCTRL, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Titel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		gbSizer8.Add( self.m_staticText19, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titleTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.m_titleTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_button21 = wx.Button( self, wx.ID_ANY, u"Filter anwenden", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.m_button21, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"Produktionsdatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		gbSizer8.Add( self.m_staticText20, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_productionDateOperatorCBChoices = [ u"=", u">", u"<" ]
		self.m_productionDateOperatorCB = wx.ComboBox( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, m_productionDateOperatorCBChoices, 0 )
		gbSizer8.Add( self.m_productionDateOperatorCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_productionDateDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer8.Add( self.m_productionDateDP, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Scandatum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		gbSizer8.Add( self.m_staticText21, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_scandateOperatorCBChoices = [ u"=", u">", u"<" ]
		self.m_scandateOperatorCB = wx.ComboBox( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, m_scandateOperatorCBChoices, 0 )
		gbSizer8.Add( self.m_scandateOperatorCB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_scanDateDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer8.Add( self.m_scanDateDP, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"Kennung", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )

		gbSizer8.Add( self.m_staticText22, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennungTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer8.Add( self.m_kennungTB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer8.AddGrowableCol( 2 )
		gbSizer8.AddGrowableRow( 6 )

		self.SetSizer( gbSizer8 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button21.Bind( wx.EVT_BUTTON, self.applyFilter )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def applyFilter( self, event ):
		event.Skip()


###########################################################################
## Class gEditInfoBitDialog
###########################################################################

class gEditInfoBitDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 317,304 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer12 = wx.GridBagSizer( 0, 0 )
		gbSizer12.SetFlexibleDirection( wx.BOTH )
		gbSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer8 = wx.StdDialogButtonSizer()
		self.m_sdbSizer8OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer8.AddButton( self.m_sdbSizer8OK )
		self.m_sdbSizer8Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer8.AddButton( self.m_sdbSizer8Cancel )
		m_sdbSizer8.Realize()

		gbSizer12.Add( m_sdbSizer8, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.BOTTOM|wx.EXPAND, 5 )

		self.m_staticText35 = wx.StaticText( self, wx.ID_ANY, u"Infodatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )

		gbSizer12.Add( self.m_staticText35, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_infoDatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT|wx.adv.DP_SHOWCENTURY )
		gbSizer12.Add( self.m_infoDatumDP, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText36 = wx.StaticText( self, wx.ID_ANY, u"Infoquelle:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )

		gbSizer12.Add( self.m_staticText36, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_infoquelleTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer12.Add( self.m_infoquelleTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText37 = wx.StaticText( self, wx.ID_ANY, u"Infotext:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText37.Wrap( -1 )

		gbSizer12.Add( self.m_staticText37, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_infoTextTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		gbSizer12.Add( self.m_infoTextTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer12.AddGrowableCol( 1 )
		gbSizer12.AddGrowableRow( 2 )

		self.SetSizer( gbSizer12 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class gGroupsDialog
###########################################################################

class gGroupsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Gruppen", pos = wx.DefaultPosition, size = wx.Size( 762,530 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer13 = wx.GridBagSizer( 0, 0 )
		gbSizer13.SetFlexibleDirection( wx.BOTH )
		gbSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText38 = wx.StaticText( self, wx.ID_ANY, u"Gruppen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )

		gbSizer13.Add( self.m_staticText38, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_groupsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer13.Add( self.m_groupsLCTRL, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_newGroupBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_newGroupBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_newGroupBU, 0, wx.ALL, 5 )

		self.m_editGroupBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editGroupBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_editGroupBU, 0, wx.ALL, 5 )

		self.m_deleteGroupBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deleteGroupBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_deleteGroupBU, 0, wx.ALL, 5 )


		gbSizer13.Add( bSizer10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer10 = wx.StdDialogButtonSizer()
		self.m_sdbSizer10OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer10.AddButton( self.m_sdbSizer10OK )
		m_sdbSizer10.Realize()

		gbSizer13.Add( m_sdbSizer10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer13.AddGrowableCol( 0 )
		gbSizer13.AddGrowableRow( 1 )

		self.SetSizer( gbSizer13 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_groupsLCTRL.Bind( wx.EVT_LEFT_DCLICK, self.editGroup )
		self.m_newGroupBU.Bind( wx.EVT_BUTTON, self.addNewGroup )
		self.m_editGroupBU.Bind( wx.EVT_BUTTON, self.editGroup )
		self.m_deleteGroupBU.Bind( wx.EVT_BUTTON, self.removeGroup )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def editGroup( self, event ):
		event.Skip()

	def addNewGroup( self, event ):
		event.Skip()


	def removeGroup( self, event ):
		event.Skip()


###########################################################################
## Class gGroupEditDialog
###########################################################################

class gGroupEditDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Gruppe bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 401,187 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer14 = wx.GridBagSizer( 0, 0 )
		gbSizer14.SetFlexibleDirection( wx.BOTH )
		gbSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText39 = wx.StaticText( self, wx.ID_ANY, u"Typ:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )

		gbSizer14.Add( self.m_staticText39, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_typeCBChoices = []
		self.m_typeCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_typeCBChoices, 0 )
		gbSizer14.Add( self.m_typeCB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText40 = wx.StaticText( self, wx.ID_ANY, u"Bezeichnung:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )

		gbSizer14.Add( self.m_staticText40, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_nameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer14.Add( self.m_nameTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"Ordnungsnummer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )

		gbSizer14.Add( self.m_staticText41, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_orderNumberSPCTRL = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 0 )
		gbSizer14.Add( self.m_orderNumberSPCTRL, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer11 = wx.StdDialogButtonSizer()
		self.m_sdbSizer11OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer11.AddButton( self.m_sdbSizer11OK )
		self.m_sdbSizer11Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer11.AddButton( self.m_sdbSizer11Cancel )
		m_sdbSizer11.Realize()

		gbSizer14.Add( m_sdbSizer11, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )


		gbSizer14.AddGrowableCol( 1 )
		gbSizer14.AddGrowableRow( 3 )

		self.SetSizer( gbSizer14 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_sdbSizer11OK.Bind( wx.EVT_BUTTON, self.editok )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def editok( self, event ):
		event.Skip()


###########################################################################
## Class gPictureFilterDialog
###########################################################################

class gPictureFilterDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bildfilter", pos = wx.DefaultPosition, size = wx.Size( 559,213 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer15 = wx.GridBagSizer( 0, 0 )
		gbSizer15.SetFlexibleDirection( wx.BOTH )
		gbSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer11 = wx.StdDialogButtonSizer()
		self.m_sdbSizer11OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer11.AddButton( self.m_sdbSizer11OK )
		self.m_sdbSizer11Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer11.AddButton( self.m_sdbSizer11Cancel )
		m_sdbSizer11.Realize()

		gbSizer15.Add( m_sdbSizer11, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 4 ), wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )

		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u"Kennummer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )

		gbSizer15.Add( self.m_staticText44, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennummerTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.m_kennummerTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText45 = wx.StaticText( self, wx.ID_ANY, u"Bildtitel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )

		gbSizer15.Add( self.m_staticText45, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titelTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.m_titelTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText46 = wx.StaticText( self, wx.ID_ANY, u"Bildgruppe:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )

		gbSizer15.Add( self.m_staticText46, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_groupCBChoices = []
		self.m_groupCB = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_groupCBChoices, 0 )
		gbSizer15.Add( self.m_groupCB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText47 = wx.StaticText( self, wx.ID_ANY, u"Aufgenommen am:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )

		gbSizer15.Add( self.m_staticText47, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_dayTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_dayTB.SetToolTip( u"Geben si ehier den Tag des Aufnahmedatums ein oder lassen sie das Feld leer wenn das Datum nicht so exakt bekannt ist" )

		gbSizer15.Add( self.m_dayTB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_monthTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.m_monthTB, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_yearTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_yearTB.SetToolTip( u"geben sie hier das Jahr des Aufnahmedatums ein oder lassen sie das Feld leer wenn nicht nach derm Aufnahmedatum gescuht werden soll." )

		gbSizer15.Add( self.m_yearTB, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer15.AddGrowableCol( 1 )
		gbSizer15.AddGrowableCol( 2 )
		gbSizer15.AddGrowableCol( 3 )

		self.SetSizer( gbSizer15 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class gEditSignifcPictureDialog
###########################################################################

class gEditSignifcPictureDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bildzuordnung an Person bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 517,252 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer16 = wx.GridBagSizer( 0, 0 )
		gbSizer16.SetFlexibleDirection( wx.BOTH )
		gbSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText52 = wx.StaticText( self, wx.ID_ANY, u"Kennung:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )

		gbSizer16.Add( self.m_staticText52, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennungTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer16.Add( self.m_kennungTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText53 = wx.StaticText( self, wx.ID_ANY, u"Titel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )

		gbSizer16.Add( self.m_staticText53, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titleTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer16.Add( self.m_titleTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText54 = wx.StaticText( self, wx.ID_ANY, u"Position an Person:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )

		gbSizer16.Add( self.m_staticText54, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_positionSPC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0 )
		gbSizer16.Add( self.m_positionSPC, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText55 = wx.StaticText( self, wx.ID_ANY, u"Untertitel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )

		gbSizer16.Add( self.m_staticText55, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_subtitleTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer16.Add( self.m_subtitleTB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer12 = wx.StdDialogButtonSizer()
		self.m_sdbSizer12OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer12.AddButton( self.m_sdbSizer12OK )
		self.m_sdbSizer12Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer12.AddButton( self.m_sdbSizer12Cancel )
		m_sdbSizer12.Realize()

		gbSizer16.Add( m_sdbSizer12, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )


		gbSizer16.AddGrowableCol( 1 )

		self.SetSizer( gbSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class gDocumentFilterDialog
###########################################################################

class gDocumentFilterDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dokumentfilter", pos = wx.DefaultPosition, size = wx.Size( 630,257 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer15 = wx.GridBagSizer( 0, 0 )
		gbSizer15.SetFlexibleDirection( wx.BOTH )
		gbSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer11 = wx.StdDialogButtonSizer()
		self.m_sdbSizer11OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer11.AddButton( self.m_sdbSizer11OK )
		self.m_sdbSizer11Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer11.AddButton( self.m_sdbSizer11Cancel )
		m_sdbSizer11.Realize()

		gbSizer15.Add( m_sdbSizer11, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )

		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u"Kennummer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )

		gbSizer15.Add( self.m_staticText44, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennummerTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.m_kennummerTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText45 = wx.StaticText( self, wx.ID_ANY, u"Dokumenttitel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )

		gbSizer15.Add( self.m_staticText45, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titelTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer15.Add( self.m_titelTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText46 = wx.StaticText( self, wx.ID_ANY, u"Dokumentgruppe:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )

		gbSizer15.Add( self.m_staticText46, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_groupCBChoices = []
		self.m_groupCB = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_groupCBChoices, 0 )
		gbSizer15.Add( self.m_groupCB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText47 = wx.StaticText( self, wx.ID_ANY, u"Produziert am:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )

		gbSizer15.Add( self.m_staticText47, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_prodDateDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DROPDOWN )
		gbSizer15.Add( self.m_prodDateDP, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText97 = wx.StaticText( self, wx.ID_ANY, u"Dokumenttyp:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText97.Wrap( -1 )

		gbSizer15.Add( self.m_staticText97, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_docTypeCBChoices = []
		self.m_docTypeCB = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_docTypeCBChoices, 0 )
		gbSizer15.Add( self.m_docTypeCB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer15.AddGrowableCol( 1 )

		self.SetSizer( gbSizer15 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class gWantedPosterPrintDialog
###########################################################################

class gWantedPosterPrintDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Einstellungen zur Steckbriefproduktion", pos = wx.DefaultPosition, size = wx.Size( 834,474 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer17 = wx.GridBagSizer( 0, 0 )
		gbSizer17.SetFlexibleDirection( wx.BOTH )
		gbSizer17.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_personenL = wx.StaticText( self, wx.ID_ANY, u"Personen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_personenL.Wrap( -1 )

		gbSizer17.Add( self.m_personenL, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_personsCHLBChoices = []
		self.m_personsCHLB = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_personsCHLBChoices, wx.LB_MULTIPLE )
		self.m_personsCHLB.SetToolTip( u"Markierte Personen werden bei der Steckbriefproduktion behandelt" )

		self.m_menu5 = wx.Menu()
		self.m_menuItem11 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Alle markieren", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem11 )

		self.m_menuItem12 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Alle Markierungen entfernen", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem12 )

		self.m_menuItem13 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"Alle mit diesem Familiennamen markieren", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.Append( self.m_menuItem13 )

		self.m_personsCHLB.Bind( wx.EVT_RIGHT_DOWN, self.m_personsCHLBOnContextMenu )

		gbSizer17.Add( self.m_personsCHLB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 5 )

		self.m_newPagePerPersoneCB = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_newPagePerPersoneCB.SetValue(True)
		gbSizer17.Add( self.m_newPagePerPersoneCB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )

		self.m_staticText59 = wx.StaticText( self, wx.ID_ANY, u"Signifikante Bilder hinzufügen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText59.Wrap( -1 )

		gbSizer17.Add( self.m_staticText59, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText65 = wx.StaticText( self, wx.ID_ANY, u"Dokumentinfos hinzufügen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText65.Wrap( -1 )

		gbSizer17.Add( self.m_staticText65, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText66 = wx.StaticText( self, wx.ID_ANY, u"Bildinfos hinzufügen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText66.Wrap( -1 )

		gbSizer17.Add( self.m_staticText66, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_addPictureInfosCB = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_addPictureInfosCB, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_addDocinfoCB = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_addDocinfoCB, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_addSignificantPicturesCB = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_addSignificantPicturesCB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText60 = wx.StaticText( self, wx.ID_ANY, u"Anzahl Bilder/Person:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText60.Wrap( -1 )

		gbSizer17.Add( self.m_staticText60, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_numPicsPerPersSPCT = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 3 )
		gbSizer17.Add( self.m_numPicsPerPersSPCT, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"Bildgröße:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )

		gbSizer17.Add( self.m_staticText62, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_6x9RB = wx.RadioButton( self, wx.ID_ANY, u"6x9cm", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		bSizer13.Add( self.m_6x9RB, 0, wx.ALL, 5 )

		self.m_9X13RB = wx.RadioButton( self, wx.ID_ANY, u"9x13cm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.m_9X13RB, 0, wx.ALL, 5 )


		gbSizer17.Add( bSizer13, wx.GBPosition( 3, 5 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText58 = wx.StaticText( self, wx.ID_ANY, u"Dateiname für Ergebnis:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText58.Wrap( -1 )

		gbSizer17.Add( self.m_staticText58, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_targetFileFPI = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Wähle eine Datei aus", u"*.pdf", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
		gbSizer17.Add( self.m_targetFileFPI, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer17.Add( self.m_staticline1, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 6 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText57 = wx.StaticText( self, wx.ID_ANY, u"Neue Seite je Person:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText57.Wrap( -1 )

		gbSizer17.Add( self.m_staticText57, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_createPostersBU = wx.Button( self, wx.ID_ANY, u"Verarbeitung starten", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_createPostersBU, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_closeBU = wx.Button( self, wx.ID_ANY, u"Schließen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_closeBU, wx.GBPosition( 8, 5 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_percdoneGA = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_percdoneGA.SetValue( 0 )
		gbSizer17.Add( self.m_percdoneGA, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 6 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


		gbSizer17.AddGrowableCol( 1 )
		gbSizer17.AddGrowableCol( 3 )
		gbSizer17.AddGrowableCol( 5 )
		gbSizer17.AddGrowableRow( 0 )

		self.SetSizer( gbSizer17 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.checkAll, id = self.m_menuItem11.GetId() )
		self.Bind( wx.EVT_MENU, self.removeAllChecks, id = self.m_menuItem12.GetId() )
		self.Bind( wx.EVT_MENU, self.checkAllOfFamily, id = self.m_menuItem13.GetId() )
		self.m_createPostersBU.Bind( wx.EVT_BUTTON, self.doPrinting )
		self.m_closeBU.Bind( wx.EVT_BUTTON, self.doClose )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def checkAll( self, event ):
		event.Skip()

	def removeAllChecks( self, event ):
		event.Skip()

	def checkAllOfFamily( self, event ):
		event.Skip()

	def doPrinting( self, event ):
		event.Skip()

	def doClose( self, event ):
		event.Skip()

	def m_personsCHLBOnContextMenu( self, event ):
		self.m_personsCHLB.PopupMenu( self.m_menu5, event.GetPosition() )


###########################################################################
## Class gDataCheckerDialog
###########################################################################

class gDataCheckerDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Datenprüfung", pos = wx.DefaultPosition, size = wx.Size( 521,381 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		gbSizer18 = wx.GridBagSizer( 0, 0 )
		gbSizer18.SetFlexibleDirection( wx.BOTH )
		gbSizer18.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_picturesCB = wx.CheckBox( self, wx.ID_ANY, u"Bilder", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_picturesCB.SetValue(True)
		bSizer17.Add( self.m_picturesCB, 0, wx.ALL, 5 )

		self.m_documentsCB = wx.CheckBox( self, wx.ID_ANY, u"Dokumente", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_documentsCB.SetValue(True)
		bSizer17.Add( self.m_documentsCB, 0, wx.ALL, 5 )

		self.m_personsCB = wx.CheckBox( self, wx.ID_ANY, u"Personen", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_personsCB.SetValue(True)
		bSizer17.Add( self.m_personsCB, 0, wx.ALL, 5 )


		gbSizer18.Add( bSizer17, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText63 = wx.StaticText( self, wx.ID_ANY, u"Durchzuführende Prüfungen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )

		gbSizer18.Add( self.m_staticText63, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_button44 = wx.Button( self, wx.ID_ANY, u"Start Prüfungen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer18.Add( self.m_button44, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer18.Add( self.m_staticline2, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText65 = wx.StaticText( self, wx.ID_ANY, u"Ergebnisse:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText65.Wrap( -1 )

		gbSizer18.Add( self.m_staticText65, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_chkResultsTCTR = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		gbSizer18.Add( self.m_chkResultsTCTR, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer18.AddGrowableCol( 1 )
		gbSizer18.AddGrowableRow( 5 )

		bSizer16.Add( gbSizer18, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button44.Bind( wx.EVT_BUTTON, self.doStartChecks )
		self.m_chkResultsTCTR.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.errorTreeItemActivated )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def doStartChecks( self, event ):
		event.Skip()

	def errorTreeItemActivated( self, event ):
		event.Skip()


###########################################################################
## Class gArchiveExtractDialog
###########################################################################

class gArchiveExtractDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Archiv Extrahieren", pos = wx.DefaultPosition, size = wx.Size( 611,221 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer21 = wx.GridBagSizer( 0, 0 )
		gbSizer21.SetFlexibleDirection( wx.BOTH )
		gbSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_doPicturesCB = wx.CheckBox( self, wx.ID_ANY, u"Bilder: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		gbSizer21.Add( self.m_doPicturesCB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_doDocumentsCB = wx.CheckBox( self, wx.ID_ANY, u"Dokumente:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		gbSizer21.Add( self.m_doDocumentsCB, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText69 = wx.StaticText( self, wx.ID_ANY, u"Gruppe:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText69.Wrap( -1 )

		gbSizer21.Add( self.m_staticText69, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_pictureGroupCBChoices = []
		self.m_pictureGroupCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_pictureGroupCBChoices, wx.CB_READONLY )
		self.m_pictureGroupCB.Enable( False )

		gbSizer21.Add( self.m_pictureGroupCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_documentGroupCBChoices = []
		self.m_documentGroupCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_documentGroupCBChoices, wx.CB_READONLY )
		self.m_documentGroupCB.Enable( False )

		gbSizer21.Add( self.m_documentGroupCB, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText70 = wx.StaticText( self, wx.ID_ANY, u"Scandatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText70.Wrap( -1 )

		gbSizer21.Add( self.m_staticText70, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		m_pictureScandateOPChoices = [ u"=", u">", u"<" ]
		self.m_pictureScandateOP = wx.ComboBox( self, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, m_pictureScandateOPChoices, wx.CB_READONLY )
		self.m_pictureScandateOP.Enable( False )

		bSizer18.Add( self.m_pictureScandateOP, 0, wx.ALL, 5 )

		self.m_pictureScandateDaySC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 31, 1 )
		self.m_pictureScandateDaySC.Enable( False )

		bSizer18.Add( self.m_pictureScandateDaySC, 0, wx.ALL, 5 )

		self.m_pictureScandateMonthSC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 12, 1 )
		self.m_pictureScandateMonthSC.Enable( False )

		bSizer18.Add( self.m_pictureScandateMonthSC, 0, wx.ALL, 5 )

		self.m_pictureScandateYearSC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2020, 2100, 2024 )
		self.m_pictureScandateYearSC.Enable( False )

		bSizer18.Add( self.m_pictureScandateYearSC, 0, wx.ALL, 5 )


		gbSizer21.Add( bSizer18, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer181 = wx.BoxSizer( wx.HORIZONTAL )

		m_documentScandateOpCBChoices = [ u"=", u">", u"<" ]
		self.m_documentScandateOpCB = wx.ComboBox( self, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, m_documentScandateOpCBChoices, wx.CB_READONLY )
		bSizer181.Add( self.m_documentScandateOpCB, 0, wx.ALL, 5 )

		self.m_documentScandateDaySC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 31, 1 )
		self.m_documentScandateDaySC.Enable( False )

		bSizer181.Add( self.m_documentScandateDaySC, 0, wx.ALL, 5 )

		self.m_documentScandateMonthSC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 12, 1 )
		self.m_documentScandateMonthSC.Enable( False )

		bSizer181.Add( self.m_documentScandateMonthSC, 0, wx.ALL, 5 )

		self.m_documentScandateYearSC = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2020, 2100, 2024 )
		self.m_documentScandateYearSC.Enable( False )

		bSizer181.Add( self.m_documentScandateYearSC, 0, wx.ALL, 5 )


		gbSizer21.Add( bSizer181, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer21.Add( self.m_staticline3, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText701 = wx.StaticText( self, wx.ID_ANY, u"Zielverzeichnis:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText701.Wrap( -1 )

		gbSizer21.Add( self.m_staticText701, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_targetDirDIRP = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Selektiere ein Verzeichnis", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
		gbSizer21.Add( self.m_targetDirDIRP, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_startExtractionBU = wx.Button( self, wx.ID_ANY, u"Start Extraktion", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer21.Add( self.m_startExtractionBU, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_abortExtractionBU = wx.Button( self, wx.ID_ANY, u"Abbrechen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer21.Add( self.m_abortExtractionBU, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_extractionGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_extractionGAUGE.SetValue( 0 )
		gbSizer21.Add( self.m_extractionGAUGE, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( gbSizer21 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_doPicturesCB.Bind( wx.EVT_CHECKBOX, self.picturesChecked )
		self.m_doDocumentsCB.Bind( wx.EVT_CHECKBOX, self.documentsChecked )
		self.m_targetDirDIRP.Bind( wx.EVT_DIRPICKER_CHANGED, self.targetDirChanged )
		self.m_startExtractionBU.Bind( wx.EVT_BUTTON, self.startExtraction )
		self.m_abortExtractionBU.Bind( wx.EVT_BUTTON, self.abortExtraction )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def picturesChecked( self, event ):
		event.Skip()

	def documentsChecked( self, event ):
		event.Skip()

	def targetDirChanged( self, event ):
		event.Skip()

	def startExtraction( self, event ):
		event.Skip()

	def abortExtraction( self, event ):
		event.Skip()


###########################################################################
## Class gNewDbDialg
###########################################################################

class gNewDbDialg ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Neue Datenbanl anlegen", pos = wx.DefaultPosition, size = wx.Size( 367,155 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		wbSizer90 = wx.GridBagSizer( 0, 0 )
		wbSizer90.SetFlexibleDirection( wx.BOTH )
		wbSizer90.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		self.m_staticText71 = wx.StaticText( self, wx.ID_ANY, u"Name der neuen DB", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		wbSizer90.Add( self.m_staticText71, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText72 = wx.StaticText( self, wx.ID_ANY, u"Aktuelle DB kopieren", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )

		wbSizer90.Add( self.m_staticText72, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_createDbBU = wx.Button( self, wx.ID_ANY, u"Jetzt anlegen", wx.DefaultPosition, wx.DefaultSize, 0 )
		wbSizer90.Add( self.m_createDbBU, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALIGN_LEFT|wx.ALL, 5 )

		self.m_cancelBU = wx.Button( self, wx.ID_ANY, u"Schließen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_cancelBU.SetHelpText( u"Den Vorgang abbrechen" )

		wbSizer90.Add( self.m_cancelBU, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_copyOldCB = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		wbSizer90.Add( self.m_copyOldCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_execuringG = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_execuringG.SetValue( 0 )
		wbSizer90.Add( self.m_execuringG, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_LEFT|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_newNameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		wbSizer90.Add( self.m_newNameTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		wbSizer90.AddGrowableCol( 1 )
		wbSizer90.AddGrowableRow( 2 )

		self.SetSizer( wbSizer90 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_createDbBU.Bind( wx.EVT_BUTTON, self.createNewDbNow )
		self.m_cancelBU.Bind( wx.EVT_BUTTON, self.cancelNewDbCeation )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def createNewDbNow( self, event ):
		event.Skip()

	def cancelNewDbCeation( self, event ):
		event.Skip()


###########################################################################
## Class mChangeDbDialog
###########################################################################

class mChangeDbDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Zu Datenbank wechseln", pos = wx.DefaultPosition, size = wx.Size( 613,451 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer23 = wx.GridBagSizer( 0, 0 )
		gbSizer23.SetFlexibleDirection( wx.BOTH )
		gbSizer23.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		m_sdbSizer13 = wx.StdDialogButtonSizer()
		self.m_sdbSizer13OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer13.AddButton( self.m_sdbSizer13OK )
		self.m_sdbSizer13Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer13.AddButton( self.m_sdbSizer13Cancel )
		m_sdbSizer13.Realize()

		gbSizer23.Add( m_sdbSizer13, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText73 = wx.StaticText( self, wx.ID_ANY, u"Datenbanken", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText73.Wrap( -1 )

		gbSizer23.Add( self.m_staticText73, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.mDatabasesLBCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		self.mDatabasesLBCTRL.SetMinSize( wx.Size( 300,200 ) )

		gbSizer23.Add( self.mDatabasesLBCTRL, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer23.AddGrowableCol( 1 )
		gbSizer23.AddGrowableRow( 0 )

		self.SetSizer( gbSizer23 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.mDatabasesLBCTRL.Bind( wx.EVT_LIST_ITEM_ACTIVATED, self.OnDatabaseActivated )
		self.mDatabasesLBCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnDatabaseSelected )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnDatabaseActivated( self, event ):
		event.Skip()

	def OnDatabaseSelected( self, event ):
		event.Skip()


###########################################################################
## Class gAboutDialog
###########################################################################

class gAboutDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Über AncPicDb", pos = wx.DefaultPosition, size = wx.Size( 566,572 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer24 = wx.GridBagSizer( 0, 0 )
		gbSizer24.SetFlexibleDirection( wx.BOTH )
		gbSizer24.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.mAboutHTMLWIN = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		gbSizer24.Add( self.mAboutHTMLWIN, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer14 = wx.StdDialogButtonSizer()
		self.m_sdbSizer14OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer14.AddButton( self.m_sdbSizer14OK )
		m_sdbSizer14.Realize()

		gbSizer24.Add( m_sdbSizer14, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer24.AddGrowableCol( 0 )
		gbSizer24.AddGrowableRow( 0 )

		self.SetSizer( gbSizer24 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class gExportDataDialog
###########################################################################

class gExportDataDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Datenexport", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer25 = wx.GridBagSizer( 0, 0 )
		gbSizer25.SetFlexibleDirection( wx.BOTH )
		gbSizer25.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText74 = wx.StaticText( self, wx.ID_ANY, u"Zielverzeichnis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText74.Wrap( -1 )

		self.m_staticText74.SetHelpText( u"Zielverzeichnis für die Exportdaten. Am besten mit dem Button rechts auswählen." )

		gbSizer25.Add( self.m_staticText74, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText75 = wx.StaticText( self, wx.ID_ANY, u"Filtereinstellungen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText75.Wrap( -1 )

		gbSizer25.Add( self.m_staticText75, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_personsCB = wx.CheckBox( self, wx.ID_ANY, u"Personen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_personsCB.SetValue(True)
		self.m_personsCB.Enable( False )

		gbSizer25.Add( self.m_personsCB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_documentsCB = wx.CheckBox( self, wx.ID_ANY, u"Dokumente", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_documentsCB.SetValue(True)
		self.m_documentsCB.Enable( False )

		gbSizer25.Add( self.m_documentsCB, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_picturesCB = wx.CheckBox( self, wx.ID_ANY, u"Bilder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_picturesCB.SetValue(True)
		self.m_picturesCB.Enable( False )

		gbSizer25.Add( self.m_picturesCB, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText77 = wx.StaticText( self, wx.ID_ANY, u"Nur Elemente neuer als:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText77.Wrap( -1 )

		gbSizer25.Add( self.m_staticText77, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_onlyNewerThanDPI = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT|wx.adv.DP_DROPDOWN )
		self.m_onlyNewerThanDPI.Enable( False )

		gbSizer25.Add( self.m_onlyNewerThanDPI, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_targetDIRP = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Auswahl des Zielverzeichnisses", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
		gbSizer25.Add( self.m_targetDIRP, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer25.Add( self.m_staticline4, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText76 = wx.StaticText( self, wx.ID_ANY, u"Fortschritt", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText76.Wrap( -1 )

		gbSizer25.Add( self.m_staticText76, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_workDoneGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_workDoneGAUGE.SetValue( 0 )
		gbSizer25.Add( self.m_workDoneGAUGE, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_bgresultTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer25.Add( self.m_bgresultTB, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer25.Add( self.m_staticline5, wx.GBPosition( 11, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.mCloseBU = wx.Button( self, wx.ID_ANY, u"Schließen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.mCloseBU.SetToolTip( u"Schließt den Dialog" )

		gbSizer25.Add( self.mCloseBU, wx.GBPosition( 12, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_startExportBU = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_startExportBU.Enable( False )
		self.m_startExportBU.SetToolTip( u"Startet den CSV-Export" )

		gbSizer25.Add( self.m_startExportBU, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_abortExportBU = wx.Button( self, wx.ID_ANY, u"Abbrechen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_abortExportBU.Enable( False )

		gbSizer25.Add( self.m_abortExportBU, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer25.AddGrowableCol( 1 )

		self.SetSizer( gbSizer25 )
		self.Layout()
		gbSizer25.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.doCloseDialog )
		self.m_targetDIRP.Bind( wx.EVT_DIRPICKER_CHANGED, self.targetDirChanged )
		self.mCloseBU.Bind( wx.EVT_BUTTON, self.doClose )
		self.m_startExportBU.Bind( wx.EVT_BUTTON, self.startCsvExport )
		self.m_abortExportBU.Bind( wx.EVT_BUTTON, self.abortCsvExport )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def doCloseDialog( self, event ):
		event.Skip()

	def targetDirChanged( self, event ):
		event.Skip()

	def doClose( self, event ):
		event.Skip()

	def startCsvExport( self, event ):
		event.Skip()

	def abortCsvExport( self, event ):
		event.Skip()


###########################################################################
## Class gRegisterDialog
###########################################################################

class gRegisterDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Registererstellung", pos = wx.DefaultPosition, size = wx.Size( 550,454 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer26 = wx.GridBagSizer( 0, 0 )
		gbSizer26.SetFlexibleDirection( wx.BOTH )
		gbSizer26.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_dialButtonsDBS = wx.StdDialogButtonSizer()
		self.m_dialButtonsDBSOK = wx.Button( self, wx.ID_OK )
		m_dialButtonsDBS.AddButton( self.m_dialButtonsDBSOK )
		m_dialButtonsDBS.Realize()

		gbSizer26.Add( m_dialButtonsDBS, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_elementsLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer26.Add( self.m_elementsLCTR, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_targetfileNameFP = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"PDF-Datei (*.pdf)|*.pdf", wx.DefaultPosition, wx.DefaultSize, wx.FLP_SAVE|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
		gbSizer26.Add( self.m_targetfileNameFP, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer26.Add( self.m_staticline6, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_startWritingBU = wx.Button( self, wx.ID_ANY, u"Starten", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer26.Add( self.m_startWritingBU, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer26.Add( self.m_staticline7, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_writingGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_writingGAUGE.SetValue( 0 )
		self.m_writingGAUGE.SetToolTip( u"Fortschritt bei der Registererstellung" )

		bSizer20.Add( self.m_writingGAUGE, 0, wx.ALL, 5 )

		self.m_abortWritingBU = wx.Button( self, wx.ID_ANY, u"Abbrechen", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.m_abortWritingBU, 0, wx.ALL, 5 )


		gbSizer26.Add( bSizer20, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText79 = wx.StaticText( self, wx.ID_ANY, u"Dateiname:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText79.Wrap( -1 )

		gbSizer26.Add( self.m_staticText79, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_listTitle = wx.StaticText( self, wx.ID_ANY, u"Verzeichniselemente:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_listTitle.Wrap( -1 )

		gbSizer26.Add( self.m_listTitle, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer26.AddGrowableCol( 1 )
		gbSizer26.AddGrowableRow( 1 )

		self.SetSizer( gbSizer26 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_targetfileNameFP.Bind( wx.EVT_FILEPICKER_CHANGED, self.fileSelected )
		self.m_startWritingBU.Bind( wx.EVT_BUTTON, self.startWriting )
		self.m_abortWritingBU.Bind( wx.EVT_BUTTON, self.abortWriting )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def fileSelected( self, event ):
		event.Skip()

	def startWriting( self, event ):
		event.Skip()

	def abortWriting( self, event ):
		event.Skip()


###########################################################################
## Class gImportCsvDialog
###########################################################################

class gImportCsvDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"CSV-Import", pos = wx.DefaultPosition, size = wx.Size( 602,205 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer27 = wx.GridBagSizer( 0, 0 )
		gbSizer27.SetFlexibleDirection( wx.BOTH )
		gbSizer27.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer16 = wx.StdDialogButtonSizer()
		self.m_sdbSizer16OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer16.AddButton( self.m_sdbSizer16OK )
		m_sdbSizer16.Realize()

		gbSizer27.Add( m_sdbSizer16, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )

		self.m_endmsgTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer27.Add( self.m_endmsgTB, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText80 = wx.StaticText( self, wx.ID_ANY, u"Importdaten", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText80.Wrap( -1 )

		gbSizer27.Add( self.m_staticText80, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_zipfileFP = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Wähle eine ZIP-Datei", u"*.zip", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_SMALL )
		gbSizer27.Add( self.m_zipfileFP, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer27.Add( self.m_staticline8, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_startBU = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_startBU, 0, wx.ALL, 5 )

		self.m_importStateGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_importStateGAUGE.SetValue( 0 )
		bSizer22.Add( self.m_importStateGAUGE, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_abortBU = wx.Button( self, wx.ID_ANY, u"Abbruch", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_abortBU, 0, wx.ALL, 5 )


		gbSizer27.Add( bSizer22, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )

		self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer27.Add( self.m_staticline10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )


		gbSizer27.AddGrowableCol( 1 )

		self.SetSizer( gbSizer27 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_zipfileFP.Bind( wx.EVT_FILEPICKER_CHANGED, self.fileChanged )
		self.m_startBU.Bind( wx.EVT_BUTTON, self.startImport )
		self.m_abortBU.Bind( wx.EVT_BUTTON, self.abortImport )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def fileChanged( self, event ):
		event.Skip()

	def startImport( self, event ):
		event.Skip()

	def abortImport( self, event ):
		event.Skip()


###########################################################################
## Class gCreateBackupDialog
###########################################################################

class gCreateBackupDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Sicherungskopie erstellen", pos = wx.DefaultPosition, size = wx.Size( 537,221 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer28 = wx.GridBagSizer( 0, 0 )
		gbSizer28.SetFlexibleDirection( wx.BOTH )
		gbSizer28.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer17 = wx.StdDialogButtonSizer()
		self.m_sdbSizer17OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer17.AddButton( self.m_sdbSizer17OK )
		m_sdbSizer17.Realize()

		gbSizer28.Add( m_sdbSizer17, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText81 = wx.StaticText( self, wx.ID_ANY, u"Zielverzeichnis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )

		gbSizer28.Add( self.m_staticText81, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_targetDirDP = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
		gbSizer28.Add( self.m_targetDirDP, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer28.Add( self.m_staticline10, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_startBackupBU = wx.Button( self, wx.ID_ANY, u"Starte Sicherung", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_startBackupBU, 0, wx.ALL, 5 )

		self.m_backupGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_backupGAUGE.SetValue( 0 )
		bSizer22.Add( self.m_backupGAUGE, 100, wx.ALL, 5 )

		self.m_cancelBackupBU = wx.Button( self, wx.ID_ANY, u"Abbrechen", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_cancelBackupBU, 0, wx.ALL, 5 )


		gbSizer28.Add( bSizer22, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer28.Add( self.m_staticline11, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_statusTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer28.Add( self.m_statusTB, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer28.AddGrowableCol( 1 )

		self.SetSizer( gbSizer28 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_targetDirDP.Bind( wx.EVT_DIRPICKER_CHANGED, self.targetDirChanged )
		self.m_startBackupBU.Bind( wx.EVT_BUTTON, self.startBackup )
		self.m_cancelBackupBU.Bind( wx.EVT_BUTTON, self.abortBackup )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def targetDirChanged( self, event ):
		event.Skip()

	def startBackup( self, event ):
		event.Skip()

	def abortBackup( self, event ):
		event.Skip()


###########################################################################
## Class gConnectedPersonsDialog
###########################################################################

class gConnectedPersonsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Verbundene Personen", pos = wx.DefaultPosition, size = wx.Size( 756,363 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer29 = wx.GridBagSizer( 0, 0 )
		gbSizer29.SetFlexibleDirection( wx.BOTH )
		gbSizer29.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer18 = wx.StdDialogButtonSizer()
		self.m_sdbSizer18OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer18.AddButton( self.m_sdbSizer18OK )
		m_sdbSizer18.Realize()

		gbSizer29.Add( m_sdbSizer18, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText82 = wx.StaticText( self, wx.ID_ANY, u"Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82.Wrap( -1 )

		gbSizer29.Add( self.m_staticText82, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText83 = wx.StaticText( self, wx.ID_ANY, u"Titel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText83.Wrap( -1 )

		gbSizer29.Add( self.m_staticText83, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_pictureNameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer29.Add( self.m_pictureNameTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_connPersLAB = wx.StaticText( self, wx.ID_ANY, u"Zugeordnete Personen", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_connPersLAB.Wrap( -1 )

		gbSizer29.Add( self.m_connPersLAB, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_connectionsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer29.Add( self.m_connectionsLCTRL, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_newPersonConnBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_newPersonConnBU.SetBitmap( wx.Bitmap( u"ressources/Add-Link.png", wx.BITMAP_TYPE_ANY ) )
		self.m_newPersonConnBU.Hide()

		bSizer23.Add( self.m_newPersonConnBU, 0, wx.ALL, 5 )

		self.m_removePersonConnBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removePersonConnBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Link.png", wx.BITMAP_TYPE_ANY ) )
		self.m_removePersonConnBU.Enable( False )

		bSizer23.Add( self.m_removePersonConnBU, 0, wx.ALL, 5 )


		gbSizer29.Add( bSizer23, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_pictureIdTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer29.Add( self.m_pictureIdTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer29.AddGrowableCol( 1 )
		gbSizer29.AddGrowableRow( 2 )

		self.SetSizer( gbSizer29 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_connectionsLCTRL.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.connectionDeselected )
		self.m_connectionsLCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.connectionSelected )
		self.m_newPersonConnBU.Bind( wx.EVT_BUTTON, self.addPersonConn )
		self.m_removePersonConnBU.Bind( wx.EVT_BUTTON, self.removePersonConn )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def connectionDeselected( self, event ):
		event.Skip()

	def connectionSelected( self, event ):
		event.Skip()

	def addPersonConn( self, event ):
		event.Skip()

	def removePersonConn( self, event ):
		event.Skip()


###########################################################################
## Class gFindPersonsDialog
###########################################################################

class gFindPersonsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Person(en) hinzufügen", pos = wx.DefaultPosition, size = wx.Size( 397,344 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer30 = wx.GridBagSizer( 0, 0 )
		gbSizer30.SetFlexibleDirection( wx.BOTH )
		gbSizer30.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_sdbSizer19 = wx.StdDialogButtonSizer()
		self.m_sdbSizer19OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer19.AddButton( self.m_sdbSizer19OK )
		self.m_sdbSizer19Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer19.AddButton( self.m_sdbSizer19Cancel )
		m_sdbSizer19.Realize()

		gbSizer30.Add( m_sdbSizer19, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText85 = wx.StaticText( self, wx.ID_ANY, u"Vorname", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85.Wrap( -1 )

		gbSizer30.Add( self.m_staticText85, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_firstNameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer30.Add( self.m_firstNameTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText86 = wx.StaticText( self, wx.ID_ANY, u"Nachname", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86.Wrap( -1 )

		gbSizer30.Add( self.m_staticText86, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_nameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer30.Add( self.m_nameTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_searchBU = wx.Button( self, wx.ID_ANY, u"Suchen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer30.Add( self.m_searchBU, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_searchResultLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer30.Add( self.m_searchResultLCTRL, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer30.AddGrowableCol( 1 )

		self.SetSizer( gbSizer30 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_searchBU.Bind( wx.EVT_BUTTON, self.doSearch )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def doSearch( self, event ):
		event.Skip()


