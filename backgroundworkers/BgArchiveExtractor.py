import wx
from pathlib import Path

from backgroundworkers.BgBasics import *
from backgroundworkers.BgWorker import BgWorker

class ArchExtractorParas():
    def __init__(self, objects_lst, docarchive):
        self.objects = objects_lst
        self.docarchive = docarchive
        self.targetpath = None
        self.group = None
        self.scandateOp = None
        self.scandateday = None
        self.scandatemonth = None
        self.scandateyear = None

class BgArchiveExtractor(BgWorker):
    def __init__(self, notifywin, paras : ArchExtractorParas):
        super().__init__(notifywin)
        self.paras = paras

    def run(self):
        try:
            objs = self.paras.objects
            da = self.paras.docarchive
            max = len(objs)
            ct = 0
            oldperc = 0
            for obj in objs:
                ct += 1
                extname = da.extract_file(obj.filepath, self.paras.targetpath)
                extpath = Path(extname)
                targname = Path(extpath.parent, obj.readableid + extpath.suffix)
                extpath.rename(targname)
                perc = int(ct/max * 100)
                if perc != oldperc:
                    wx.PostEvent(self.notifywin, NotifyPercentEvent(perc))
                    oldperc = perc

                if self.abortrequested:
                    wx.PostEvent(self.notifywin, ResultEvent(None))
                    return
        finally:
            wx.PostEvent(self.notifywin, NotifyPercentEvent(100))
            wx.PostEvent(self.notifywin, ResultEvent(ct))