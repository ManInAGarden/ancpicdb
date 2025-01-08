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
        recc = len(pics_r)
        assert recc >= 3


        fo = tf.NamedTemporaryFile(mode="w+t", prefix="TST", suffix=".csv")
        with fo:
            expo = sqp.SQLitePersistCsvExporter(Picture, fo)
            lc = expo.do_export(pics_r)
            r_recc = 0
            fo.seek(0)
            lines = fo.readlines()
            assert len(lines) == recc + 1


    def test_simpleExport02(self):
        titles = ["ExportPic01", "ExportPic02", "ExportPic03", "ExportPic04"]
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
                                                      & sqp.IsLike(Picture.Title, "ExportPic%")).as_list()
        recc = len(pics_r)
        assert recc >= 4


        fo = tf.NamedTemporaryFile(mode="w+t", prefix="TST", suffix=".csv", delete = False)
        with fo:
            expo = sqp.SQLitePersistCsvExporter(Picture, fo)
            lc = expo.do_export(pics_r)
            assert lc == recc
            r_recc = 0
            fo.seek(0)
            lines = fo.readlines()
            assert len(lines) == recc + 1


    def test_simpleExpNImport01(self):
        titles = ["ExImportPic01", "ExImportPic02", "ExImportPic03", "ExImportPic04"]
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
                                                      & sqp.IsLike(Picture.Title, "ExImportPic%")).as_list()
        recc = len(pics_r)
        assert recc >= 4

        fo = tf.NamedTemporaryFile(mode="w+t", prefix="TST", suffix=".csv", delete = False)
        with fo:
            expo = sqp.SQLitePersistCsvExporter(Picture, fo)
            lc = expo.do_export(pics_r)
            assert lc == recc
            r_recc = 0
            fo.seek(0)

            #remove the data from the test DB (we still have a copy in pics_r)
            for picr in pics_r:
                self.Spf.delete(picr) 

            impo = sqp.SQLitePersistCsvImporter(Picture, self.Spf)
            impo.do_import(fo)

            #now read the data again
            pics_r2 = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1970) 
                                                      & sqp.IsLike(Picture.Title, "ExImportPic%")).as_list()
            
            #and now check that all data are the same
            assert len(pics_r)==len(pics_r2)

            for i in range(len(pics_r)):
                assert pics_r[i]._id == pics_r2[i]._id
                assert pics_r[i].title == pics_r2[i].title


