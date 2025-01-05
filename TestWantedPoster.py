import unittest
import datetime as dt
from tempfile import TemporaryDirectory
from TestBase import TestBase
from PersistClasses import FullPerson, Person
from WantedPoster import WantedPoster


class TestWantedPoster(unittest.TestCase):
    
    def setUp(self):
        super().setUp()

    def test_write_gustaf(self):
        pfath = Person(name = "Gründgens", firstname="Arnold Hubert")
        pmoth = Person(name="Gründgens", firstname = "Emmi")

        it = "Er war ein deutscher Theater- und Filmschauspieler sowie Sänger und Regisseur. Besondere Bekanntheit erlangte er in seiner Rolle als Mephistopheles in Goethes Faust und als Interpret des Schlagers Die Nacht ist nicht allein zum Schlafen da (1938). In der Zeit des Nationalsozialismus wurde er vom preußischen Ministerpräsidenten Hermann Göring gefördert und protegiert. Ab 1934 war Gründgens Intendant des Berliner Schauspielhauses, von 1937 bis 1945 Generalintendant der Preußischen Staatstheater. Nach dem Zweiten Weltkrieg setzte er seine Karriere fort, war von 1947 bis 1951 Generalintendant der Städtischen Bühnen Düsseldorf, dann bis 1955 erster Geschäftsführer des Neuen Schauspiels Düsseldorf und anschließend bis 1963 Generalintendant des Deutschen Schauspielhauses in Hamburg."
        it += " Gründgens war das Vorbild für die Figur des Hendrik Höfgen in Klaus Manns Roman Mephisto (1936) und dem darauf beruhenden Filmdrama (1981) von István Szabó. Sein postmortaler Persönlichkeitsschutz war Gegenstand der sogenannten Mephisto-Entscheidung des Bundesverfassungsgerichts."
        it += "\nQuelle Wikipedia"
        p1 = FullPerson(name = "Gründgens", 
                    firstname = "Gustav",
                    rufname = "Gustaf",
                    birthdate = dt.datetime(1899, 12, 22),
                    deathdate = dt.datetime(1963, 10, 7),
                    infotext = it,
                    mother = pmoth,
                    father = pfath)
        pl = [p1]
        wp = WantedPoster(pl, "testwantedposterGustaf.pdf")
        wp.do_create()

    def _add_fchild(self, p, lname, fname, bdate=None):
        if p.childrenasfather is None:
            p.childrenasfather = []
        cp = Person(firstname = fname,
                    name = lname,
                    birthdate=bdate)
        p.childrenasfather.append(cp)

    def test_write_mick(self):
        pfath = Person(name = "Jagger", firstname="Basil Fanshowe", rufname="Joe", birthyear=1913, deathyear=2006)
        pmoth = Person(name="Jagger", firstname = "Eva Ensley Mary", nameofbirth="Scutts", birthyear=1913, deathyear=2000)

        it = "ist ein britischer Musiker, Sänger und Songwriter. Berühmt wurde er als Frontmann der britischen Rockgruppe The Rolling Stones. Jagger spielt Mundharmonika, Gitarre und Klavier. Er wirkte auch als Schauspieler, Produzent und Komponist bei mehreren Filmen mit."
        it += "Mick Jagger gilt als der 'Inbegriff des ewig jungen Rockstars'."
        it += "\nQuelle Wikipedia"
        p1 = FullPerson(name = "Jagger", 
                    firstname = "Michael Phillip",
                    rufname = "Mick",
                    birthdate = dt.datetime(1943, 7, 26),
                    infotext = it,
                    mother = pmoth,
                    father = pfath)
        
        self._add_fchild(p1, "Jagger", "Karis", dt.datetime(1970,11,4))
        self._add_fchild(p1, "Jagger", "Jade", dt.datetime(1971,10,21))
        self._add_fchild(p1, "Jagger", "Elisabeth Scarlett", dt.datetime(1984,3,2))
        self._add_fchild(p1, "Jagger", "James Leroy Augustin", dt.datetime(1985,8,28))
        self._add_fchild(p1, "Jagger", "Georgia May Ayeesha", dt.datetime(1992,1,12))
        self._add_fchild(p1, "Jagger", "Gabriel Luke Beauregard ", dt.datetime(1997,12,9))
        self._add_fchild(p1, "Jagger", "Lucas Maurice Morad", dt.datetime(1999,5,18))
        self._add_fchild(p1, "Jagger", "Deveraux Octavian Basil", dt.datetime(2016,12,8))
         
        
        pl = [p1]
        wp = WantedPoster(pl, None, "testwantedposterMick.pdf")
        wp.do_create()