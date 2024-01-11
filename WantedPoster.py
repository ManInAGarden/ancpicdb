
import copy
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER
import PIL as pil

from PersistClasses import Person, FullPerson
from DocArchiver import DocArchiver

class WantedPoster(object):
    
    class PosterConfig(object):
        def __init__(self):
            self.newpgperperson = False
            self.targetfile = None
            self.includepics = False
            self.maxpic = 3

    def __init__(self, plist : list, archiver : DocArchiver, tmppath : str, config : PosterConfig = None):
        self.styles = getSampleStyleSheet()

        if config is None:
            self._posterconfig = WantedPoster.PosterConfig()
        else:
            self._posterconfig = config
        
        self._archtemp = tmppath
        self._archiver = archiver

        #Schmutzabweiser        
        if plist is None or len(plist) == 0:
            raise Exception("No valid list of persons was provied.")
        
        fname = self._posterconfig.targetfile
        if fname is None or len(fname)==0:
            raise Exception("No valid filename for the pdf to be created was provided")

        self._title = "Personenprofile"
        self._pageinfo = "AncPicDb Profildruck"

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
    
    def _get_qualified_pics(self, allpics) -> list:
        """Returns a sorted list of qualified pics for printing
        """
        answ = []
        for pic in allpics:
            #a picture which is qualified hast an ordernum > 0 and a subtitle
            if pic.subtitle is not None \
                and len(pic.subtitle)>0 \
                    and pic.position>0:
                answ.append(pic)

        answ.sort(key=lambda x : x.position)

        return answ

    def _get_besttakendate(self, pic):
        if pic.takendate is not None:
            return "({:%d.%m.%Y})".format(pic.takendate)

        if pic.fluftakenyear is not None and pic.fluftakenyear > 0:
            if pic.fluftakenmonth is not None and pic.fluftakenmonth.code!="NOMONTH":
                return "({} {})".format(pic.fluftakenmonth.value, pic.fluftakenyear)
            else:
                return "({})".format(pic.fluftakenyear)
            
        return ""

    def _calc_subtitle(self, pic):
        dt = self._get_besttakendate(pic.picture)
        return "{} {}".format(pic.subtitle, dt)

    def _get_optimal_imagesize(self, fname : str, desiwidth, desiheight) -> tuple():
        with pil.Image.open(fname) as img: 
            width, height = img.size
        
        #aussuming 300dpi we calculate the size of the pictures when printed on paper
        width = inch*width/300.0
        height = inch*height/300.0

        wfact = 1.0
        hfact = 1.0
        wfact = desiwidth/width
        hfact = desiheight/height

        if wfact < hfact:
            fact = wfact
        else:
            fact = hfact

        return (width*fact, height*fact)

    def _add_pictures(self, story : list, pics : list = None):
        if pics is None or len(pics) == 0:
            return #nothing to do
        
        qualipics = self._get_qualified_pics(pics)

        if qualipics is None or len(qualipics)<=0:
            return
        
        bstyle = self.styles["BodyText"]
        head1s = self.styles["Heading1"]
        head3s = self.styles["Heading2"]
        itstyle = self.styles["Italic"]
        picsub = ParagraphStyle(self.styles["Normal"], alignment=TA_CENTER)
        
        story.append(Paragraph("Bilder", head3s))
        for pic in qualipics:
            #append picture
            
            path_to_file = self._archiver.extract_file(pic.picture.filepath, self._archtemp)
            w,h = self._get_optimal_imagesize(path_to_file, 13.0*cm, 13.0*cm)
            story.append(Image(path_to_file, w, h))
            st = self._calc_subtitle(pic)
            story.append(Paragraph(st, style=picsub))
            #append subitle

    def do_create(self):
        story = [Spacer(1, 2.0*cm)]
        bstyle = self.styles["BodyText"]
        head1s = self.styles["Heading1"]
        head3s = self.styles["Heading2"]
        itstyle = self.styles["Italic"]
        
        pl = self._plist
        for p in pl:
            self._addparagraph(story, head1s, p.name + ", " + p.firstname)

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
                self._addparagraph(story, head3s, "Kinder")
                for child in children:
                    self._addparagraph(story, bstyle, self._getshortinfo(child))

            #handle significant pictures
            if self._posterconfig.includepics:
                self._add_pictures(story, p.pictures)

            #At the end we attach a pagebreak or some space to separate the persons' data
            if not self._posterconfig.newpgperperson:
                story.append(Spacer(1, 2.0*cm))
            else:
                story.append(PageBreak())
                

        self._doc.build(story)

    def _addparagraph(self, story, style, txt : str = None ):
        if txt is None:
            return
        
        txt = txt.replace('\n','<br />')
        txt = txt.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;')

        pg = Paragraph(txt, style)
        story.append(pg)