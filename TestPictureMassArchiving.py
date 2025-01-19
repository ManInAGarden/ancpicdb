import unittest
import backgroundworkers as bw
from TestBase import TestBase

class TestPictureMassArchiving(TestBase):
    
    def setUp(self):
        super().setUp()

    def _mock_paras(self) -> {}:
        paras = {}
        paras["fact"] = self.Spf
        paras["files"] = []
        paras["logger"] = self.MyLogger #it's a class variable in the base class and its populated in setUpClass()
        paras["docarchiver"] = self.Archiver #same here
        paras["machlabel"] = "TEST"

        return paras

    def test_title_generation(self):
        paras = self._mock_paras()
        mabw = bw.BgPictureMassArchiving(None, paras) 

        tit = "Hallo WeltIckMagDir01"
        titr = mabw._calc_title(tit)
        assert titr == "Hallo Welt Ick Mag Dir 01"

        tit = "Die Wiener Sängerknaben16und32"
        titr = mabw._calc_title(tit)
        assert titr == "Die Wiener Sängerknaben 16 und 32"

        tit = "Unschuldige_AngeklageSindErst schuldig_wenn der Richter dies 1x verkündet."
        titr = mabw._calc_title(tit)
        assert titr == "Unschuldige Angeklage Sind Erst schuldig wenn der Richter dies 1 x verkündet"

        tit = "c:\irgendwo\DieseDatei.warum_auch_immer.txt"
        titr = mabw._calc_title(tit)
        assert titr == "Diese Datei.warum auch immer"


    def test_create_read_id(self):
        paras = self._mock_paras()
        mabw = bw.BgPictureMassArchiving(None, paras) 

        oldid = mabw._create_readid()
        assert oldid is not None
        for i in range(30):
            id = mabw._create_readid()
            assert id != oldid
            oldid = id
