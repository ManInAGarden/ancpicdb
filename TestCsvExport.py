import sqlitepersist as sqp
from TestBase import TestBase
from PersistClasses import Picture, FluffyMonthCat
import datetime as dt
import unittest
import tempfile as tf

class TestCsvExport(TestBase):
    def setUp(self):
        super().setUp()
        

    def test_simpleExport01(self):
        titles = ["ExportLikeQuerPic01", "ExportLikeQuerPic02", "ExportLikeQuerPic03", "ExportNotQueryPic04"]
        monthes = ["MONTH09", "MONTH10", "MONTH11", "MONTH12"]
        tm = 0
        for tit in titles:
            moca = self.Spf.getcat(FluffyMonthCat, monthes[tm])
            pic = self.Mck.create_picture(title=tit, scandate=dt.datetime.now(),
                                          yeartaken=1970,
                                          monthtaken=moca)
            tm += 1
            self.Spf.flush(pic)

        pics_r = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1970) 
                                                      & sqp.IsLike(Picture.Title, "%Like%")).as_list()
        assert len(pics_r) == 3


        fo = tf.NamedTemporaryFile(mode="w+t", prefix="TST", suffix=".csv")
        with fo:
            expo = sqp.SQLitePersistCsvExporter(Picture, fo)
            expo.do_export(pics_r)