import sqlitepersist as sqp
from TestBase import TestBase
from PersistClasses import Picture, FluffyMonthCat, Person, SexCat, PersonPictureInter
import datetime as dt
import unittest
import tempfile as tf
import time
import uuid

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

            impo = sqp.SQLitePersistCsvImporter(Picture, self.Spf, logger=self.MyLogger)
            impo.do_import(fo)

            #now read the data again
            pics_r2 = sqp.SQQuery(self.Spf, Picture).where((Picture.FlufTakenYear==1970) 
                                                      & sqp.IsLike(Picture.Title, "ExImportPic%")).as_list()
            
            #and now check that all data are the same
            assert len(pics_r)==len(pics_r2)

            for i in range(len(pics_r)):
                assert pics_r[i]._id == pics_r2[i]._id
                assert pics_r[i].title == pics_r2[i].title

    def test_simpleExpNImWithKey900(self):
        firstnames = ["900First_Fritz", "900First_Maria", "900_First_Karl", "900First_Anna"]
        lastnames = ["900Last_Lang", "900Last_Callas", "900Last_Valentin", "900Last_Held"]
        sexes = ["MALE", "FEMALE", "MALE", "FEMALE"]
        birthdays = [5, 2, 4, 8]
        birthsmonthes = [12, 12, 6, 3]
        birthyears = [1890, 1923, 1882, 1873]
        deathyears = [1976, 1977, 1948, 1918]

        tm = 0
        for firstname in firstnames:
            pers = self.Mck.create_person(firstname=firstname,
                                          name = lastnames[tm],
                                          biosex_code=sexes[tm],
                                          birthday=birthdays[tm],
                                          birthmonth=birthsmonthes[tm],
                                          birthyear=birthyears[tm])
            pers.deathyear = deathyears[tm]
            pers2 = self.Mck.create_person(firstname=firstname + "_NOTTHESAME", #second pers has different first name
                                          name = lastnames[tm],
                                          biosex_code=sexes[tm],
                                          birthday=birthdays[tm],
                                          birthmonth=birthsmonthes[tm],
                                          birthyear=birthyears[tm])
            tm += 1
            self.Spf.flush(pers)
            self.Spf.flush(pers2)

        time.sleep(5) #sleep five seconds so that lastupd will be newer then created on the import
        #now get all the persons with a not empty deathyear
        person1s = sqp.SQQuery(self.Spf, Person).where(sqp.IsNotNone(Person.DeathYear)).as_list()
        
        assert len(person1s) > 0

        fo = tf.NamedTemporaryFile(mode="w+t", prefix="TST", suffix=".csv", delete = False)
        with fo:
            expo = sqp.SQLitePersistCsvExporter(Person, fo)
            lc = expo.do_export(person1s)
            assert lc > 0
            
            fo.seek(0)
            #try an update by first and last name as identifier and NOT with the _id
            impo = sqp.SQLitePersistCsvImporter(Person, 
                                                self.Spf, 
                                                findwith=[Person.FirstName, Person.Name],
                                                logger=self.MyLogger)
            impct = impo.do_import(fo)
            assert impo.imported is not None
            assert impct > 0

            assert type(impo.imported[0]) is uuid.UUID

        assert len(person1s) == impct

        person1s_r = sqp.SQQuery(self.Spf, Person).where(sqp.IsNotNone(Person.DeathYear)).as_list()

        assert len(person1s_r) == len(person1s)

        #we did not change anything in the csv, so data should be basically the same after the import
        for pind in range(len(person1s_r)):
            p1s = person1s[pind]
            p1sr = person1s_r[pind]
            assert p1s._id == p1sr._id
            assert p1s.name == p1sr.name
            assert p1s.firstname == p1sr.firstname
            assert p1s.birthdate == p1sr.birthdate
            assert p1s.created == p1sr.created
            #but!
            assert p1s.lastupdate < p1sr.lastupdate #there should me more than 5s between the two
            
    
    def test_intersExpNImWithKey910(self):
        mykey = "910"
        pdt = [
            {"firstname":"First_Fritz", "name":"Last_Lang", "biosex":"MALE","birthday":5,"birthmonth":12,"birthyear":1890, "deathyear":1976},
            {"firstname":"First_Maria", "name":"Last_Callas", "biosex":"FEMALE","birthday":2, "birthmonth":12, "birthyear":1923, "deathyear":1977},
            {"firstname":"First_Karl", "name":"Last_Valentin", "biosex":"MALE","birthday":4, "birthmonth": 6, "birthyear":1892, "deathyear":1948}
        ]
        
        newpdt = [
            {"firstname":"First_Anna", "name":"Last_Held", "biosex":"MALE","birthday": 8,"birthmonth": 3,"birthyear": 1873, "deathyear":1918}
        ]

        persons = self.Mck.create_persons(pdt, mykey)

        picd = [
            {"title":"Maria auf der großen Bühne", "fluftakenyear":1923},
            {"title":"Karl in München", "fluftakenyear": 1910},
            {"title":"Fritz im Regiesessel beim Dreh von Metropolis", "fluftakenyear":1921},
            {"title":"Anna beim Vorsprechen", "fluftakenyear": 1893},
            {"title":"Anna bei sonstwas", "fluftakenyear": 1994}
        ]

        pictures = self.Mck.create_pictures(picd, mykey)

        inter1 = self.Mck.intersect_persnpic(persons[0], pictures[2], subtitle="Fritz", key=mykey)
        inter2 = self.Mck.intersect_persnpic(persons[1], pictures[0], subtitle="Maria", key=mykey)
        inter3 = self.Mck.intersect_persnpic(persons[2], pictures[1], subtitle="Karl", key=mykey)

        time.sleep(5) #sleep five seconds so that lastupd will be newer then created on the import
        #now get all the persons with a not empty deathyear, that should be only those defined in pdt
        person1s = sqp.SQQuery(self.Spf, Person).where(sqp.IsNotNone(Person.DeathYear) & sqp.IsLike(Person.Name, mykey + "%")).as_list()
        pict1s = sqp.SQQuery(self.Spf, PersonPictureInter).where(sqp.IsLike(PersonPictureInter.Subtitle, mykey + "%")).as_list()
        assert len(person1s) > 0
        assert len(pict1s) > 0


        fo = tf.NamedTemporaryFile(mode="w+t", prefix="TSTPER", suffix=".csv", delete = False)
        with fo:
            expo = sqp.SQLitePersistCsvExporter(Person, fo)
            lc = expo.do_export(person1s)
            assert lc > 0

            fo2 = tf.NamedTemporaryFile(mode="w+t", prefix="TSTPIC", suffix=".csv", delete = False)
            with fo2:
                #export the old persons
                expo2 = sqp.SQLitePersistCsvExporter(PersonPictureInter, fo2)
                lc2 = expo2.do_export(pict1s)
            
                assert lc2 > 0

                #create a new person in the db wwhich should completely be left alone by imports
                newpersons = self.Mck.create_persons(newpdt, "910")
                newpersons_r = sqp.SQQuery(self.Spf, Person).where(sqp.IsNotNone(Person.DeathYear) & sqp.IsLike(Person.Name, mykey + "%")).as_list()
                assert len(newpersons_r) == len(newpersons) + len(person1s)

                #connect a new person not in the csv to a new picture
                inter4 = self.Mck.intersect_persnpic(newpersons[0], pictures[3], subtitle="Anna", key="910") 
                #connect to an old person, this should be deleted by the import when restricted
                inter5 = self.Mck.intersect_persnpic(persons[2], pictures[4], subtitle="Simulierte alte Verknüpfung", key="910") #connect an old person to another picture
                
                pict2s = sqp.SQQuery(self.Spf, PersonPictureInter).where(sqp.IsLike(PersonPictureInter.Subtitle, "910%")).as_list()
                assert len(pict1s) + 2 == len(pict2s) #two more connections after the export here
                
                fo.seek(0)
                #try import by _id
                persimpo = sqp.SQLitePersistCsvImporter(Person, 
                                                    self.Spf,
                                                    logger=self.MyLogger)
                
                impct = persimpo.do_import(fo)
                assert impct == len(persimpo.imported)
                assert impct > 0
                assert impct == len(person1s) #the new person was not exported and so also not imported?

                fo2.seek(0)
                #import person->picture intersects beeing strict on the PersonId, which means
                #that any connection from person to picture that is not on the csv will
                #be deleted when it connects to person that is mentioned in at least one of the 
                #intersections in the csv
                impinters = sqp.SQLitePersistCsvImporter(PersonPictureInter, 
                                                    self.Spf,
                                                    logger=self.MyLogger)
                impct2 = impinters.do_import(fo2)
                assert impct2 > 0
                impct3 = impinters.restrict_on(persimpo.imported, PersonPictureInter.PersonId)
                assert impct3 == len(impinters.imported)

        assert len(person1s) == impct

        person1s_r = sqp.SQQuery(self.Spf, Person).where(sqp.IsNotNone(Person.DeathYear) & sqp.IsLike(Person.Name, mykey + "%")).as_list()

        assert len(person1s_r) == len(person1s) + 1 #there's one additional person?

        #we did not change anything in the csv, so data should be basically the same after the import
        for pind in range(len(person1s)):
            p1s = person1s[pind]
            p1sr = person1s_r[pind]
            assert p1s._id == p1sr._id
            assert p1s.name == p1sr.name
            assert p1s.firstname == p1sr.firstname
            assert p1s.birthdate == p1sr.birthdate
            assert p1s.created == p1sr.created
            #but!
            assert p1s.lastupdate < p1sr.lastupdate #there should me more than 5s between the two

        #inter4 should NOT be gone becaues it connects a different person
        pict1s_r = sqp.SQQuery(self.Spf, PersonPictureInter).where(sqp.IsLike(PersonPictureInter.Subtitle, "910%")).as_list()
        assert len(pict1s) + 1 == len(pict1s_r)
        for interind in range(len(pict1s)):
            ppinter = pict1s[interind]
            ppinter_r = pict1s_r[interind]
            assert ppinter.personid == ppinter_r.personid
            assert ppinter.pictureid == ppinter_r.pictureid
            assert ppinter.subtitle == ppinter_r.subtitle
            assert ppinter.created == ppinter_r.created
            #but!
            assert ppinter.lastupdate < ppinter_r.lastupdate

        #make really sure the inter4 is still there
        inter4_r = sqp.SQQuery(self.Spf, PersonPictureInter).where(PersonPictureInter.Id==inter4._id).first_or_default(None)
        assert inter4_r is not None

        #but inter5 is gone
        inter5_r = sqp.SQQuery(self.Spf, PersonPictureInter).where(PersonPictureInter.Id==inter5._id).first_or_default(None)
        assert inter5_r is None


