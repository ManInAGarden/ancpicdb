import tempfile
import os
import wx
import wx.adv
import wx.richtext
import GeneratedGUI as gg
from PersistClasses import Person, Document
from GuiHelper import GuiHelper
import sqlitepersist as sqp

class AboutDialog(gg.gAboutDialog):
    
    def __init__(self, parent, fact : sqp.SQFactory, version, dbname, storagepath):
        super().__init__(parent)
        self._fact = fact
        self._configuration = parent._configuration
        self._version = version
        self._dbname = dbname
        self._storagepath = storagepath
        

    def showmodal(self):
        GuiHelper.set_icon(self)
        aboutfile = GuiHelper.get_ressorcefilename("About.html")
        modifabout = self.modifyhtml(aboutfile)
        self.mAboutHTMLWIN.LoadFile(modifabout)
        self.ShowModal()

    def modifyhtml(self, filename:str) -> str:
        with open(filename) as f:
            content = f.read()

        content = content.replace("VERSION", self._version)
        content = content.replace("DBNAME", self._dbname)
        content = content.replace("STORAGEPATH", self._storagepath)

        tmpdir = tempfile.gettempdir()
        tmpfilename = os.path.join(tmpdir,"aboutmodif.html")

        with open(tmpfilename,"w") as f:
            f.write(content)

        return tmpfilename