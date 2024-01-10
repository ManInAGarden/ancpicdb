# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class AncPicDBMain
###########################################################################

class AncPicDBMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"AncPicDB", pos = wx.DefaultPosition, size = wx.Size( 964,619 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )

		self.m_mainMenuBar = wx.MenuBar( 0 )
		self.m_fileMenu = wx.Menu()
		self.m_connectDbMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Verbinde Datenbank", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_connectDbMI )

		self.m_backupDbMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Sicherungskopiie erstellen", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_backupDbMI )

		self.m_fileMenu.AppendSeparator()

		self.m_exitMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Beenden"+ u"\t" + u"CTRL+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_exitMI )

		self.m_mainMenuBar.Append( self.m_fileMenu, u"Datei" )

		self.m_editMenu = wx.Menu()
		self.m_groupsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Gruppen", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_groupsMI )

		self.m_documentsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Dokumente"+ u"\t" + u"CTRL+D", u"Dokumente sichten", wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_documentsMI )

		self.m_picsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Bilder"+ u"\t" + u"CTRL+B", u"Bilder sichten", wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_picsMI )

		self.m_mainMenuBar.Append( self.m_editMenu, u"Bearbeiten" )

		self.m_menu4 = wx.Menu()
		self.m_menuItem9 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Steckbriefe produzieren", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.Append( self.m_menuItem9 )

		self.m_mainMenuBar.Append( self.m_menu4, u"Extras" )

		self.m_helpMenu = wx.Menu()
		self.m_help = wx.MenuItem( self.m_helpMenu, wx.ID_ANY, u"Hilfe", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_helpMenu.Append( self.m_help )

		self.m_aboutAncPicDB = wx.MenuItem( self.m_helpMenu, wx.ID_ANY, u"Über", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_helpMenu.Append( self.m_aboutAncPicDB )

		self.m_mainMenuBar.Append( self.m_helpMenu, u"Hilfe" )

		self.SetMenuBar( self.m_mainMenuBar )

		self.m_mainWindowSB = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		m_mainGBSIZER = wx.GridBagSizer( 0, 0 )
		m_mainGBSIZER.SetFlexibleDirection( wx.BOTH )
		m_mainGBSIZER.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_personsLBChoices = []
		self.m_personsLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_personsLBChoices, wx.LB_HSCROLL|wx.LB_NEEDED_SB )
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
		self.m_picturesLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_picturesLBChoices, 0 )
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
		self.m_documentsLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_documentsLBChoices, 0 )
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

		self.SetSizer( m_mainGBSIZER )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.backupDb, id = self.m_backupDbMI.GetId() )
		self.Bind( wx.EVT_MENU, self.quit, id = self.m_exitMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewGroupsDialog, id = self.m_groupsMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewDocumentsDialog, id = self.m_documentsMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewPicturesDialog, id = self.m_picsMI.GetId() )
		self.Bind( wx.EVT_MENU, self.printWantedPosters, id = self.m_menuItem9.GetId() )
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
		self.m_disconnectDocumentBU.Bind( wx.EVT_BUTTON, self.disconnectDocument )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def backupDb( self, event ):
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


	def disconnectDocument( self, event ):
		event.Skip()


###########################################################################
## Class geditDocumentDialog
###########################################################################

class geditDocumentDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dokument bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 806,813 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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
		m_sdbSizer3.Realize();

		gbSizer7.Add( m_sdbSizer3, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 3 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Kennummer:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		gbSizer7.Add( self.m_staticText13, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_kennummerTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.m_kennummerTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Typ:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		gbSizer7.Add( self.m_staticText14, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_doctypCBChoices = []
		self.m_doctypCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_doctypCBChoices, 0 )
		gbSizer7.Add( self.m_doctypCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText30 = wx.StaticText( self, wx.ID_ANY, u"Titel:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )

		gbSizer7.Add( self.m_staticText30, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_titelTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer7.Add( self.m_titelTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"Produktionsdatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		gbSizer7.Add( self.m_staticText15, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_produktionsDatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer7.Add( self.m_produktionsDatumDP, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Scandatum:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		gbSizer7.Add( self.m_staticText16, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Informationen:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gbSizer7.Add( self.m_staticText18, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_zusatzinfoLCT = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer7.Add( self.m_zusatzinfoLCT, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

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
		gbSizer7.Add( self.m_scanDatumDP, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText181 = wx.StaticText( self, wx.ID_ANY, u"Dokument:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181.Wrap( -1 )

		gbSizer7.Add( self.m_staticText181, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_archivepathTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer7.Add( self.m_archivepathTB, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_docextTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer7.Add( self.m_docextTB, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

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


		gbSizer7.Add( bSizer6, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer7.AddGrowableCol( 1 )
		gbSizer7.AddGrowableRow( 7 )

		self.SetSizer( gbSizer7 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_addPictBitInfoBU.Bind( wx.EVT_BUTTON, self.addInfoBit )
		self.m_editPictBitInfoBU.Bind( wx.EVT_BUTTON, self.editInfoBit )
		self.m_deletePictBitInfoBU.Bind( wx.EVT_BUTTON, self.removeInfoBit )
		self.m_uploadBU.Bind( wx.EVT_BUTTON, self.uploadDocument )
		self.m_viewDocumentBU.Bind( wx.EVT_BUTTON, self.viewDocument )
		self.m_downloadBU.Bind( wx.EVT_BUTTON, self.downloadDocument )
		self.m_button23.Bind( wx.EVT_BUTTON, self.removeDocument )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def addInfoBit( self, event ):
		event.Skip()

	def editInfoBit( self, event ):
		event.Skip()

	def removeInfoBit( self, event ):
		event.Skip()

	def uploadDocument( self, event ):
		event.Skip()

	def viewDocument( self, event ):
		event.Skip()

	def downloadDocument( self, event ):
		event.Skip()

	def removeDocument( self, event ):
		event.Skip()


###########################################################################
## Class gDocumentsViewDialog
###########################################################################

class gDocumentsViewDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Dokumente sichten", pos = wx.DefaultPosition, size = wx.Size( 930,566 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_documentsLBChoices = []
		self.m_documentsLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_documentsLBChoices, wx.LB_HSCROLL|wx.LB_SINGLE )
		gbSizer6.Add( self.m_documentsLB, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_ApplyFilterBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_ApplyFilterBU.SetBitmap( wx.Bitmap( u"ressources/Filled-Filter.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_ApplyFilterBU, 0, wx.ALL, 5 )

		self.m_addRowBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addRowBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_addRowBU, 0, wx.ALL, 5 )

		self.m_editBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_editBU, 0, wx.ALL, 5 )

		self.m_downloadPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_downloadPictureBU.SetBitmap( wx.Bitmap( u"ressources/Download.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_downloadPictureBU, 0, wx.ALL, 5 )

		self.deletePictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.deletePictureBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.deletePictureBU, 0, wx.ALL, 5 )


		gbSizer6.Add( bSizer10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Dokumente:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer6.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		m_sdbSizer2.Realize();

		gbSizer6.Add( m_sdbSizer2, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 0 )
		gbSizer6.AddGrowableRow( 1 )

		self.SetSizer( gbSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_documentsLB.Bind( wx.EVT_LISTBOX_DCLICK, self.editElement )
		self.m_addRowBU.Bind( wx.EVT_BUTTON, self.addNewRow )
		self.m_editBU.Bind( wx.EVT_BUTTON, self.editElement )
		self.m_downloadPictureBU.Bind( wx.EVT_BUTTON, self.downloadPicture )
		self.deletePictureBU.Bind( wx.EVT_BUTTON, self.removeRow )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def editElement( self, event ):
		event.Skip()

	def addNewRow( self, event ):
		event.Skip()


	def downloadPicture( self, event ):
		event.Skip()

	def removeRow( self, event ):
		event.Skip()


###########################################################################
## Class geditPictureDialog
###########################################################################

class geditPictureDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bild bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 737,798 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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
		m_sdbSizer3.Realize();

		gbSizer7.Add( m_sdbSizer3, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 4 ), wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )

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
		gbSizer7.Add( self.m_bitmapPAN, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 3 ), wx.EXPAND |wx.ALL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_uploadBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_uploadBU.SetBitmap( wx.Bitmap( u"ressources/Upload.png", wx.BITMAP_TYPE_ANY ) )
		self.m_uploadBU.SetToolTip( u"Ein Bild von der lokalen Festplatte hochladen" )

		bSizer6.Add( self.m_uploadBU, 0, wx.ALL, 5 )

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

		self.SetSizer( gbSizer7 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_zusatzinfoLCT.Bind( wx.EVT_LEFT_DCLICK, self.editInfoBit )
		self.m_addPictBitInfoBU.Bind( wx.EVT_BUTTON, self.addInfoBit )
		self.m_editPictBitInfoBU.Bind( wx.EVT_BUTTON, self.editInfoBit )
		self.m_deletePictBitInfoBU.Bind( wx.EVT_BUTTON, self.removeInfoBit )
		self.m_uploadBU.Bind( wx.EVT_BUTTON, self.uploadDocument )
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

	def uploadDocument( self, event ):
		event.Skip()

	def removePicture( self, event ):
		event.Skip()


###########################################################################
## Class gPicturesViewDialog
###########################################################################

class gPicturesViewDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bilder sichten", pos = wx.DefaultPosition, size = wx.Size( 919,606 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Bilder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer6.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_picturesLBChoices = []
		self.m_picturesLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_picturesLBChoices, wx.LB_SINGLE )
		gbSizer6.Add( self.m_picturesLB, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_applyFilterBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_applyFilterBU.SetBitmap( wx.Bitmap( u"ressources/Filled-Filter.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_applyFilterBU, 0, wx.ALL, 5 )

		self.m_addPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addPictureBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_addPictureBU, 0, wx.ALL, 5 )

		self.m_editBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_editBU, 0, wx.ALL, 5 )

		self.m_downloadPictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_downloadPictureBU.SetBitmap( wx.Bitmap( u"ressources/Download.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_downloadPictureBU, 0, wx.ALL, 5 )

		self.deletePictureBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.deletePictureBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.deletePictureBU, 0, wx.ALL, 5 )


		gbSizer6.Add( bSizer10, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		m_sdbSizer2.Realize();

		gbSizer6.Add( m_sdbSizer2, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText49 = wx.StaticText( self, wx.ID_ANY, u"Filter:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText49.Wrap( -1 )

		gbSizer6.Add( self.m_staticText49, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_filterInfoTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		gbSizer6.Add( self.m_filterInfoTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 1 )
		gbSizer6.AddGrowableRow( 1 )

		self.SetSizer( gbSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_picturesLB.Bind( wx.EVT_LISTBOX_DCLICK, self.editPicture )
		self.m_applyFilterBU.Bind( wx.EVT_BUTTON, self.applyFilter )
		self.m_addPictureBU.Bind( wx.EVT_BUTTON, self.addNewPicture )
		self.m_editBU.Bind( wx.EVT_BUTTON, self.editPicture )
		self.m_downloadPictureBU.Bind( wx.EVT_BUTTON, self.downloadPicture )
		self.deletePictureBU.Bind( wx.EVT_BUTTON, self.removePicture )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def editPicture( self, event ):
		event.Skip()

	def applyFilter( self, event ):
		event.Skip()

	def addNewPicture( self, event ):
		event.Skip()


	def downloadPicture( self, event ):
		event.Skip()

	def removePicture( self, event ):
		event.Skip()


###########################################################################
## Class gPersonEditDialog
###########################################################################

class gPersonEditDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Person bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 939,649 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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

		self.m_infotextTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_WORDWRAP )
		self.m_infotextTB.SetMinSize( wx.Size( -1,100 ) )
		self.m_infotextTB.SetMaxSize( wx.Size( 400,300 ) )

		gbSizer2.Add( self.m_infotextTB, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Mutter/Vater:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		gbSizer2.Add( self.m_staticText7, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_motherCBChoices = []
		self.m_motherCB = wx.ComboBox( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, m_motherCBChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self.m_motherCB.SetSelection( 0 )
		gbSizer2.Add( self.m_motherCB, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_fatherCBChoices = []
		self.m_fatherCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_fatherCBChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		gbSizer2.Add( self.m_fatherCB, wx.GBPosition( 5, 3 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_personSDBSI = wx.StdDialogButtonSizer()
		self.m_personSDBSIOK = wx.Button( self, wx.ID_OK )
		m_personSDBSI.AddButton( self.m_personSDBSIOK )
		self.m_personSDBSICancel = wx.Button( self, wx.ID_CANCEL )
		m_personSDBSI.AddButton( self.m_personSDBSICancel )
		m_personSDBSI.Realize();

		gbSizer2.Add( m_personSDBSI, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Signifikante Bilder:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		gbSizer2.Add( self.m_staticText51, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_significantPictursLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer2.Add( self.m_significantPictursLCTRL, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_addSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Add-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_addSignPicBU, 0, wx.ALL, 5 )

		self.m_editSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Edit.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_editSignPicBU, 0, wx.ALL, 5 )

		self.m_removeSignPicBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removeSignPicBU.SetBitmap( wx.Bitmap( u"ressources/Delete-Row.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_removeSignPicBU, 0, wx.ALL, 5 )


		gbSizer2.Add( bSizer12, wx.GBPosition( 7, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Infotext:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		gbSizer2.Add( self.m_staticText12, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_bioSexCBChoices = []
		self.m_bioSexCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_bioSexCBChoices, wx.CB_READONLY )
		gbSizer2.Add( self.m_bioSexCB, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )


		gbSizer2.AddGrowableCol( 1 )
		gbSizer2.AddGrowableCol( 2 )
		gbSizer2.AddGrowableCol( 3 )
		gbSizer2.AddGrowableCol( 4 )
		gbSizer2.AddGrowableRow( 6 )

		self.SetSizer( gbSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_geburtsdatumDP.Bind( wx.adv.EVT_DATE_CHANGED, self.birthDateChanged )
		self.m_todesdatumDP.Bind( wx.adv.EVT_DATE_CHANGED, self.deathDateChanged )
		self.m_addSignPicBU.Bind( wx.EVT_BUTTON, self.addPicture )
		self.m_editSignPicBU.Bind( wx.EVT_BUTTON, self.editPictureInfo )
		self.m_removeSignPicBU.Bind( wx.EVT_BUTTON, self.removePicture )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def birthDateChanged( self, event ):
		event.Skip()

	def deathDateChanged( self, event ):
		event.Skip()

	def addPicture( self, event ):
		event.Skip()

	def editPictureInfo( self, event ):
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
		m_sdbSizer4.Realize();

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
		m_sdbSizer4.Realize();

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

		m_operatorCBChoices = [ u"=", u">", u"<" ]
		self.m_operatorCB = wx.ComboBox( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, m_operatorCBChoices, 0 )
		gbSizer8.Add( self.m_operatorCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_productionDateDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer8.Add( self.m_productionDateDP, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Scandatum", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		gbSizer8.Add( self.m_staticText21, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_comboBox5Choices = [ u"=", u">", u"<" ]
		self.m_comboBox5 = wx.ComboBox( self, wx.ID_ANY, u"=", wx.DefaultPosition, wx.DefaultSize, m_comboBox5Choices, 0 )
		gbSizer8.Add( self.m_comboBox5, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

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

	def __del__( self ):
		pass


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
		m_sdbSizer8.Realize();

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
		m_sdbSizer10.Realize();

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
		m_sdbSizer11.Realize();

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
		m_sdbSizer11.Realize();

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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bildzuordnung an Person bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 349,189 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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
		m_sdbSizer12.Realize();

		gbSizer16.Add( m_sdbSizer12, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_RIGHT|wx.EXPAND, 5 )


		gbSizer16.AddGrowableCol( 1 )

		self.SetSizer( gbSizer16 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class gWantedPosterPrintDialog
###########################################################################

class gWantedPosterPrintDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Einstellungen zur Steckbriefproduktion", pos = wx.DefaultPosition, size = wx.Size( 594,355 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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

		gbSizer17.Add( self.m_personsCHLB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_newPagePerPersoneCB = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_newPagePerPersoneCB.SetValue(True)
		gbSizer17.Add( self.m_newPagePerPersoneCB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_LEFT|wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer17.Add( self.m_staticline1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText57 = wx.StaticText( self, wx.ID_ANY, u"Neue Seite je Person:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText57.Wrap( -1 )

		gbSizer17.Add( self.m_staticText57, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_createPostersBU = wx.Button( self, wx.ID_ANY, u"Verarbeitung starten", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_createPostersBU, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_closeBU = wx.Button( self, wx.ID_ANY, u"Schließen", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer17.Add( self.m_closeBU, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_percdoneGA = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_percdoneGA.SetValue( 0 )
		gbSizer17.Add( self.m_percdoneGA, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


		gbSizer17.AddGrowableCol( 1 )
		gbSizer17.AddGrowableRow( 0 )

		self.SetSizer( gbSizer17 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_createPostersBU.Bind( wx.EVT_BUTTON, self.doPrinting )
		self.m_closeBU.Bind( wx.EVT_BUTTON, self.doClose )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def doPrinting( self, event ):
		event.Skip()

	def doClose( self, event ):
		event.Skip()


