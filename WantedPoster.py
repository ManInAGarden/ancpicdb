from reportlab.pdfgen import canvas

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

#PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()


class PosterConfig(object):
    def __init__(self):
        self.newlperperson = False

class WantedPoster(object):
    def __init__(self, plist : list, fname : str, config : PosterConfig = None):
        if config is None:
            self._posterconfig = PosterConfig()
        else:
            self._posterconfig = config

        #Schmutzabweiser        
        if plist is None or len(plist) == 0:
            raise Exception("No valid list of persons was provied.")
        
        if fname is None or len(fname)==0:
            raise Exception("No valid filename for the pdf to be created was provided")

        self._title = "Hello world"
        self._pageinfo = "platypus example"

        self._plist = plist
        self._filename = fname
        self._doc = SimpleDocTemplate(fname, pagesize = A4)

    def _get_birthndeathshort(self, p):
        lifedta = ""

        if p.birthdate is not None:
            lifedta = "*{:%d.%m.%Y}".format(p.birthdate)
        elif p.birthyear is not None and p.birthyear != 0:
            if p.birthmonth is not None and p.birthmonth.code != "NOMONTH" and p.birthyear is not None:
                lifedta = "*{} {}".format(p.birthmonth.value, p.birthyear)
            else:
                lifedta = "*{}".format(p.birthyear)
        
        if len(lifedta) > 0:
            spc = " "
        else:
            spc = ""

        if p.deathdate is not None:
            lifedta += "{}+{:%d.%m.%Y}".format(spc, p.deathdate)
        else:
            if p.deathmonth is not None and p.deathmonth.code != "NOMONTH" and p.deathyear is not None:
                lifedta += "{}+{} {}".format(spc, p.deathmonth.value, p.deathyear)
            elif p.deathyear is not None and p.deathyear != 0:
                lifedta += "{}+{}".format(spc, p.deathyear)
        
        return lifedta

    def _getshortinfo(self, p):
        answ = ""
        if p.name is not None:
            answ = p.name
        else:
            "Unbekannt"

        if p.firstname is not None:
            answ += ", " + p.firstname

        if p.rufname is not None:
            answ += " (gen. {})".format(p.rufname)

        answ += " " + self._get_birthndeathshort(p)

        return answ

    def do_create(self):
        story = [Spacer(1, 2.0*cm)]
        bstyle = styles["BodyText"]
        head1style = styles["Heading1"]
        head2style = styles["Heading2"]
        itstyle = styles["Italic"]
        pl = self._plist
        for p in pl:
            self._addparagraph(story, head1style, p.name + ", " + p.firstname)

            if p.rufname is not None:
                self._addparagraph(story, itstyle, "genannt " + p.rufname)
            
            lifedta = self._get_birthndeathshort(p)
            self._addparagraph(story, bstyle, lifedta)

            if p.mother is not None:
                pmo = "Mutter: " + self._getshortinfo(p.mother)
                self._addparagraph(story, bstyle, pmo)

            if p.father is not None:
                pfa = "Vater: " + self._getshortinfo(p.father)
                self._addparagraph(story, bstyle, pfa)

            story.append(Spacer(1, 0.4*cm))
            self._addparagraph(story, bstyle, p.infotext)

            children = []
            if p.childrenasfather is not None:
                children = children + p.childrenasfather
            if p.childrenasmother is not None:
                children = children + p.childrenasmother

            if len(children) > 0:
                self._addparagraph(story, head2style, "Kinder")
                for child in children:
                    self._addparagraph(story, bstyle, self._getshortinfo(child))

            if not self._posterconfig.newlperperson:
                story.append(Spacer(1, 2.0*cm))
            else:
                story.append(PageBreak())
                

        self._doc.build(story)

    def _addparagraph(self, story, style, txt : str = None ):
        if txt is None:
            return
        
        pg = Paragraph(txt, style)
        story.append(pg)