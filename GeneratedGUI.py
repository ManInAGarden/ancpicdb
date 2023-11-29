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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"AncPicDB", pos = wx.DefaultPosition, size = wx.Size( 560,569 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )

		self.m_mainMenuBar = wx.MenuBar( 0 )
		self.m_fileMenu = wx.Menu()
		self.m_connectDbMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Verbinde Datenbank", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_connectDbMI )

		self.m_fileMenu.AppendSeparator()

		self.m_exitMI = wx.MenuItem( self.m_fileMenu, wx.ID_ANY, u"Beenden", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_fileMenu.Append( self.m_exitMI )

		self.m_mainMenuBar.Append( self.m_fileMenu, u"Datei" )

		self.m_editMenu = wx.Menu()
		self.m_picsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Bilder", u"Bilder sichten", wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_picsMI )

		self.m_documentsMI = wx.MenuItem( self.m_editMenu, wx.ID_ANY, u"Dokumente", u"Dokumente sichten", wx.ITEM_NORMAL )
		self.m_editMenu.Append( self.m_documentsMI )

		self.m_mainMenuBar.Append( self.m_editMenu, u"Bearbeiten" )

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
		self.Bind( wx.EVT_MENU, self.quit, id = self.m_exitMI.GetId() )
		self.Bind( wx.EVT_MENU, self.openViewPicturesDialog, id = self.m_picsMI.GetId() )
		self.m_newPersonBU.Bind( wx.EVT_LEFT_DOWN, self.editNewPerson )
		self.m_editPersonBU.Bind( wx.EVT_LEFT_DOWN, self.editExistingPerson )
		self.m_deletePersonBU.Bind( wx.EVT_LEFT_DOWN, self.deletePerson )
		self.m_connectPictureBU.Bind( wx.EVT_LEFT_DOWN, self.connectPicture )
		self.m_editPictureBU.Bind( wx.EVT_LEFT_DOWN, self.editPicture )
		self.m_disconnectPictureBU.Bind( wx.EVT_LEFT_DOWN, self.disconnectPicture )
		self.m_connectDocumentBU.Bind( wx.EVT_LEFT_DOWN, self.editNewDocument )
		self.m_editDocumentBU.Bind( wx.EVT_LEFT_DOWN, self.editDocument )
		self.m_disconnectDocumentBU.Bind( wx.EVT_LEFT_DOWN, self.disconnectDocument )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def quit( self, event ):
		event.Skip()

	def openViewPicturesDialog( self, event ):
		event.Skip()

	def editNewPerson( self, event ):
		event.Skip()

	def editExistingPerson( self, event ):
		event.Skip()

	def deletePerson( self, event ):
		event.Skip()

	def connectPicture( self, event ):
		event.Skip()

	def editPicture( self, event ):
		event.Skip()

	def disconnectPicture( self, event ):
		event.Skip()

	def editNewDocument( self, event ):
		event.Skip()

	def editDocument( self, event ):
		event.Skip()

	def disconnectDocument( self, event ):
		event.Skip()


###########################################################################
## Class gPicturesViewDialog
###########################################################################

class gPicturesViewDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bilder sichten", pos = wx.DefaultPosition, size = wx.Size( 522,424 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		m_picturesLBChoices = []
		self.m_picturesLB = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_picturesLBChoices, wx.LB_SINGLE )
		gbSizer6.Add( self.m_picturesLB, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_ApplyFilterBU = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_ApplyFilterBU.SetBitmap( wx.Bitmap( u"ressources/Filled-Filter.png", wx.BITMAP_TYPE_ANY ) )
		bSizer10.Add( self.m_ApplyFilterBU, 0, wx.ALL, 5 )

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


		gbSizer6.Add( bSizer10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Bilder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer6.Add( self.m_staticText11, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		m_sdbSizer2.Realize();

		gbSizer6.Add( m_sdbSizer2, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 0 )
		gbSizer6.AddGrowableRow( 1 )

		self.SetSizer( gbSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_addPictureBU.Bind( wx.EVT_BUTTON, self.addNewPicture )
		self.m_editBU.Bind( wx.EVT_BUTTON, self.editPicture )
		self.m_downloadPictureBU.Bind( wx.EVT_BUTTON, self.downloadPicture )
		self.deletePictureBU.Bind( wx.EVT_BUTTON, self.removePicture )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def addNewPicture( self, event ):
		event.Skip()

	def editPicture( self, event ):
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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Person bearbeiten", pos = wx.DefaultPosition, size = wx.Size( 479,602 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Vorname", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		gbSizer2.Add( self.m_staticText8, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		gbSizer2.Add( self.m_staticText9, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_vornameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_vornameTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_NameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_NameTB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Geburtsname:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		gbSizer2.Add( self.m_staticText10, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_geburtsnameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_geburtsnameTB, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Geboren am:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		gbSizer2.Add( self.m_staticText11, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_geburtsdatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer2.Add( self.m_geburtsdatumDP, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Verstorben am:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		gbSizer2.Add( self.m_staticText6, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_todesdatumDP = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT )
		gbSizer2.Add( self.m_todesdatumDP, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_infotextTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE )
		self.m_infotextTB.SetMinSize( wx.Size( -1,100 ) )

		gbSizer2.Add( self.m_infotextTB, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Mutter/Vater:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		gbSizer2.Add( self.m_staticText7, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_motherCBChoices = []
		self.m_motherCB = wx.ComboBox( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, m_motherCBChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self.m_motherCB.SetSelection( 0 )
		gbSizer2.Add( self.m_motherCB, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_fatherCBChoices = []
		self.m_fatherCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_fatherCBChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		gbSizer2.Add( self.m_fatherCB, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_personSDBSI = wx.StdDialogButtonSizer()
		self.m_personSDBSIOK = wx.Button( self, wx.ID_OK )
		m_personSDBSI.AddButton( self.m_personSDBSIOK )
		self.m_personSDBSICancel = wx.Button( self, wx.ID_CANCEL )
		m_personSDBSI.AddButton( self.m_personSDBSICancel )
		m_personSDBSI.Realize();

		gbSizer2.Add( m_personSDBSI, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Infotext:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		gbSizer2.Add( self.m_staticText12, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_bioSexCBChoices = []
		self.m_bioSexCB = wx.ComboBox( self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_bioSexCBChoices, wx.CB_READONLY )
		gbSizer2.Add( self.m_bioSexCB, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		gbSizer2.AddGrowableCol( 1 )
		gbSizer2.AddGrowableCol( 2 )
		gbSizer2.AddGrowableRow( 6 )

		self.SetSizer( gbSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass

