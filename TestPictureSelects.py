import datetime as dt
import unittest
from DocArchiver import DocArchiver
import sqlitepersist as sqp
from TestBase import TestBase
from PersistClasses import Picture, FluffyMonthCat

class TestPictureSelects(TestBase):
    
    def setUp(self):
        super().setUp()

    def test_updating(self):
        pic1 = self.Mck.create_picture(title="Testpic01", scandate=dt.datetime.now())
        self.Spf.flush(pic1)
        newtitle = "Omma Frieda und ihre Enkel"
        pic1.title = newtitle
        self.Spf.flush(pic1)
        pic_r = sqp.SQQuery(self.Spf, Picture).where(Picture.Id==pic1._id).first_or_default(None)
        assert pic_r is not None
        assert pic_r.title == newtitle

    def test_simple_select(self):
        titles = ["TestSelPic01", "testselpic02", "testSelPic01"]

        for title in titles:
            pic = self.Mck.create_picture(title=title, scandate=dt.datetime.now())
            self.Spf.flush(pic)

        selected = sqp.SQQuery(self.Spf, Picture).where(Picture.Title=="TestSelPic01").as_list()
        assert len(selected)==1
        assert selected[0].title == "TestSelPic01"

    def test_additive_querycreation01(self):
        titles = ["AddQuerPic01", "AddQuerPic02", "AddQuerPic03"]

        for tit in titles:
            pic = self.Mck.create_picture(title=tit, scandate=dt.datetime.now())
            self.Spf.flush(pic)

        
        exp = Picture.Title == "AddQuerPic01"
        exp2 = exp | (Picture.Title == "AddQuerPic02")

        q0 = sqp.SQQuery(self.Spf, Picture).where(sqp.IsIn(Picture.Title, ["AddQuerPic01", "AddQuerPic02"]))
        pics_r = q0.as_list()
        assert len(pics_r)==2

        q1 = sqp.SQQuery(self.Spf, Picture).where((Picture.Title=="AddQuerPic01") | (Picture.Title=="AddQuerPic02"))
        pics_r = q1.as_list()
        assert len(pics_r) == 2
        
        pics_r = sqp.SQQuery(self.Spf, Picture).where(exp2).as_list()
        assert len(pics_r)==2

    def test_additive_querycreation02(self):
        titles = ["AddQuerPic01", "AddQuerPic02", "AddQuerPic03"]
        monthes = ["MONTH09", "MONTH10", "MONTH11"]
        tm = 0
        for tit in titles:
            moca = self.Spf.getcat(FluffyMonthCat, monthes[tm])
            pic = self.Mck.create_picture(title=tit, scandate=dt.datetime.now(),
                                          yeartaken=1963,
                                          monthtaken=moca)
            tm += 1
            self.Spf.flush(pic)

        exp = Picture.FlufTakenYear==1963
        exp = exp & (Picture.FlufTakenMonth=="MONTH10")

        pics_r = sqp.SQQuery(self.Spf, Picture).where(exp).as_list()
        assert len(pics_r)==1
        pic_r = pics_r[0]
        assert pic_r.fluftakenmonth.Code=="MONTH10" and pic_r.fluftakenyear==1963

    def test_likequery01(self):
        titles = ["AddLikeQuerPic01", "AddLikeQuerPic02", "AddLikeQuerPic03", "AddNotQueryPic04"]
        monthes = ["MONTH09", "MONTH10", "MONTH11", "MONTH12"]
        tm = 0
        for tit in titles:
            moca = self.Spf.getcat(FluffyMonthCat, monthes[tm])
            pic = self.Mck.create_picture(title=tit, scandate=dt.datetime.now(),
                                          yeartaken=1965,
                                          monthtaken=moca)
            tm += 1
            self.Spf.flush(pic)

        pics_r = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1965) 
                                                      & sqp.IsLike(Picture.Title, "%Like%")).as_list()
        assert len(pics_r) == 3

        pics_r = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1965) 
                                                      & sqp.NotIsLike(Picture.Title, "%Like%")).as_list()
        assert len(pics_r) == 1
    
    def test_isnone01(self):
        titles = ["AddQuerPic10", "AddQuerPic20", "AddQuerPic30"]
        yt = 1970
        for tit in titles:
            pic = self.Mck.create_picture(title=tit, scandate=dt.datetime.now(),
                                          yeartaken=yt)
            self.Spf.flush(pic)

        pics_r = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1970)
                                                      & sqp.IsNone(Picture.ScanDate)).as_list()
        assert len(pics_r) == 0
        pics_r = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1970)
                                                      & sqp.IsNone(Picture.TakenDate)).as_list()
        assert len(pics_r) == 3
        pics_r = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1970)
                                                      &sqp.IsNotNone(Picture.ScanDate)).as_list()
        assert len(pics_r) == 3


    def test_likequeryLimited01(self):
        titles = ["LimitLikeQuerPic01", "LimitLikeQuerPic02", "LimitLikeQuerPic03", "LimitNotQueryPic04"]
        monthes = ["MONTH09", "MONTH10", "MONTH11", "MONTH12"]
        tm = 0
        for tit in titles:
            moca = self.Spf.getcat(FluffyMonthCat, monthes[tm])
            pic = self.Mck.create_picture(title=tit, scandate=dt.datetime.now(),
                                          yeartaken=1965,
                                          monthtaken=moca)
            tm += 1
            self.Spf.flush(pic)

        pics_r = sqp.SQQuery(self.Spf, Picture, limit=2).where((Picture.FlufTakenYear==1965) 
                                                            & sqp.IsLike(Picture.Title, "%Like%")).as_list()
        assert len(pics_r) == 2

        pics_r = sqp.SQQuery(self.Spf, Picture, limit=2).where((Picture.FlufTakenYear==1965) 
                                                      & sqp.NotIsLike(Picture.Title, "%Like%")).as_list()
        assert len(pics_r) == 1

        
