import datetime
from enum import Enum
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER
import PIL as pil

from PersistClasses import Person, FullPerson
from DocArchiver import DocArchiver

class PicSizeEnum(Enum):
    PS6X9 = 0
    PS9X13 = 1

class WantedPoster(object):
    
    class PosterConfig(object):
        def __init__(self):
            self.newpgperperson = False
            self.targetfile = None
            self.includepics = False
            self.includedocinfo = True #add archive info for documents related to person
            self.includepicinfo = True #add archive info for pictures related to person
            self.maxpic = 3
            self.picsize = PicSizeEnum(0)

    def __init__(self, plist : list, archiver : DocArchiver, tmppath : str, config : PosterConfig = None):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle("Heading1tog", self.styles["Heading1"], keepWithNext=True))
        self.styles.add(ParagraphStyle("Heading2tog", self.styles["Heading2"], keepWithNext=True))
        self.styles.add(ParagraphStyle("Heading3tog", self.styles["Heading3"], keepWithNext=True))

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
            #a picture which is qualified has an ordernum > 0 and a non empty subtitle
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

    def _get_optimal_imagesize(self, fname : str, desisize) -> tuple:
        if desisize == PicSizeEnum.PS6X9:
            desiheight = desiwidth = 9*cm
        elif desisize == PicSizeEnum.PS9X13:
            desiheight = desiwidth = 13*cm
        
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
    
    def _get_docinfo(self, doc) -> str:
        if doc.document is None:
            return "?"
        
        d = doc.document
        answ = d.readableid + " "

        if d.documentgroup is not None: answ += ", Gruppe: <i>" + d.documentgroup.name + "</i>"
        if d.type is not None: answ += ", Dokumentart: <i>" + d.type.value + "</i>"

        answ += ", Titel: <i>" + d.title + "</i>"

        if d.productiondate is not None: 
            answ += ", erstellt am: <i>" + "{}.{}.{}".format(d.productiondate.day, d.productiondate.month, d.productiondate.year) + "</i>"
        if d.scandate is not None: 
            answ += ", gescannt am: <i>" + "{}.{}.{}".format(d.scandate.day, d.scandate.month, d.scandate.year) + "</i>"

        return answ
    
    def _get_picinfo(self, pic) -> str:
        if pic.picture is None:
            return "?"

        p = pic.picture
        answ = p.readableid + " "

        if p.picturegroup is not None:
            answ += ", Gruppe: <i>" + p.picturegroup.name + "</i>"

        answ += ", Titel: <i>" + p.title + "</i>"
        takendate = p.best_takendate
        if takendate[2] is not None: #we have at least a year
            taks = takendate[2].__str__()
            if takendate[1] is not None:
                taks = takendate[1].__str__() + "." + taks
                if takendate[0] is not None:
                    taks = takendate[0].__str__() + "." + taks

            answ += ", aufgenommen: <i>" + taks + "</i>"

        if p.scandate is not None:
            answ += ", gescannt am: <i>" + "{}.{}.{}".format(p.scandate.day, p.scandate.month, p.scandate.year) + "</i>"

        return answ

    def _get_monthnumber(self, flufmo):
        if flufmo.code == "NOMONTH": return 1

        months = [
            "NOMONTH",
            "MONTH01",
            "MONTH02",
            "MONTH03",
            "MONTH04",
            "MONTH05",
            "MONTH06",
            "MONTH07",
            "MONTH08",
            "MONTH09",
            "MONTH10",
            "MONTH11",
            "MONTH12"
        ]

        return months.index(flufmo.code)
    
    def _sort_docbestdate(self, val):
        if val.document is None:
            return datetime.datetime.now()
        doc = val.document
        if doc.productiondate is not None:
            return doc.productiondate
        elif doc.scandate is not None:
            return doc.scandate
        else:
            return datetime.datetime.now()
        
    def _sort_picbestdate(self, val):
        if val.picture is None:
            return datetime.datetime.now()
        pic = val.picture
        if pic.takendate is not None:
            return pic.takendate
        elif pic.fluftakenyear is not None and pic.fluftakenyear != 0:
            if pic.fluftakenmonth is not None:
                m = self._get_monthnumber(pic.fluftakenmonth)
                return datetime.datetime(pic.fluftakenyear, m, 1)
            else:
                return datetime.datetime(pic.fluftakenyear, 1, 1)
        elif pic.scandate is not None:
            return pic.scandate
        else:
            return datetime.datetime.now()
        
    def _add_docinfos(self, story, documents : list = None):
        if documents is None:
            return
        
        docs = sorted(documents, key=self._sort_docbestdate)
        bstyle = self.styles["BodyText"]
        head2s = self.styles["Heading2tog"]
        itstyle = self.styles["Italic"]
        
        self._addparagraph(story, head2s, "Archivierte Dokumente")
        

        for doc in docs:
            doctxt = self._get_docinfo(doc)
            self._addparagraph(story, bstyle, doctxt)

    def _add_picinfos(self, story, pictures : list=None):
        if pictures is None:
            return
        
        pics = sorted(pictures, key=self._sort_picbestdate)
        bstyle = self.styles["BodyText"]
        head2s = self.styles["Heading2tog"]
        itstyle = self.styles["Italic"]
        
        self._addparagraph(story, head2s, "Verknüpfte Bilder")
        
        for pic in pics:
            pictxt = self._get_picinfo(pic)
            self._addparagraph(story, bstyle, pictxt)


    def _add_pictures(self, story : list, pics : list = None):
        """Add qualified pictures (a selection of the pictures) to the text"""
        if pics is None or len(pics) == 0:
            return #nothing to do
        
        qualipics = self._get_qualified_pics(pics)

        if qualipics is None or len(qualipics)<=0:
            return
        
        bstyle = self.styles["BodyText"]
        head1s = self.styles["Heading1tog"]
        head2s = self.styles["Heading2tog"]
        itstyle = self.styles["Italic"]
        picsub = ParagraphStyle(self.styles["Normal"], alignment=TA_CENTER)
        
        story.append(Paragraph("Bilder", head2s))
        picct = 0
        for pic in qualipics:
            #append picture
            picct += 1
            if picct > self._posterconfig.maxpic:
                break
            
            path_to_file = self._archiver.extract_file(pic.picture.filepath, self._archtemp)
            w,h = self._get_optimal_imagesize(path_to_file, self._posterconfig.picsize)
            img = Image(path_to_file, w, h)
            #story.append(img)
            st = self._calc_subtitle(pic)
            subt = Paragraph(st, style=picsub)
            #story.append(subt)
            #append subitle
            story.append(KeepTogether([img, subt]))
        
    def _get_children_sortkey(self, child):
        #init to the max
        byear = 20000
        bmonth = 12
        bday = 31

        if child.birthdate is not None:
            bday = child.birthdate.day
            bmonth = child.birthdate.month
            byear = child.birthdate.year
        else:
            if child.birthyear is not None and child.birthyear!=0:
                byear = child.birthyear

            if child.birthmonth is not None and child.birthmonth.code != "NOMONTH":
                bmonth = child.birthmonth._as_number()

        return (byear, bmonth, bday)

    def _get_children(self, p : FullPerson):
        children = []
        if p.childrenasfather is not None:
            children = children + p.childrenasfather
        if p.childrenasmother is not None:
            children = children + p.childrenasmother

        #now sort them by birthdate
        children.sort(key=lambda x: self._get_children_sortkey(x))
        return children

    def do_create(self):
        story = [Spacer(1, 2.0*cm)]
        bstyle = self.styles["BodyText"]
        head1s = self.styles["Heading1tog"]
        head3s = self.styles["Heading2tog"]
        itstyle = self.styles["Italic"]
        
        pl = self._plist
        for p in pl:
            self._addparagraph(story, head1s, p.name + ", " + p.firstname)

            if p.rufname is not None:
                self._addparagraph(story, itstyle, "genannt " + p.rufname)
            
            lifedta = self._get_birthndeathshort(p)
            if len(lifedta) > 0:
                self._addparagraph(story, bstyle, lifedta)

            if p.mother is not None:
                pmo = "Mutter: " + self._getshortinfo(p.mother)
                self._addparagraph(story, bstyle, pmo)

            if p.father is not None:
                pfa = "Vater: " + self._getshortinfo(p.father)
                self._addparagraph(story, bstyle, pfa)

            if p.infotext is not None and len(p.infotext) > 0:
                story.append(Spacer(1, 0.4*cm))
                self._addparagraph(story, bstyle, p.infotext)

            children = self._get_children(p)
            if len(children) > 0:
                self._addparagraph(story, head3s, "Kinder")
                childrentxt = ""
                for child in children:
                    if len(childrentxt) > 0:
                        childrentxt += "<br/>"
                    childrentxt += self._getshortinfo(child)

                self._addparagraph(story, bstyle, childrentxt)

            #handle significant pictures
            if self._posterconfig.includepics and p.pictures is not None and len(p.pictures)>0:
                self._add_pictures(story, p.pictures)

            #include information about archived documents related to the person
            if self._posterconfig.includedocinfo and p.documents is not None and len(p.documents)>0:
                self._add_docinfos(story, p.documents)

            if self._posterconfig.includepicinfo and p.pictures is not None and len(p.pictures)>0:
               self._add_picinfos(story, p.pictures)

            #At the end we attach a pagebreak or some space to separate the persons' data
            if not self._posterconfig.newpgperperson:
                story.append(Spacer(1, 2.0*cm))
            else:
                story.append(PageBreak())
                

        self._doc.build(story)

    def _addparagraph(self, story, style, txt : str = None):
        if txt is None:
            return
        
        txt = txt.replace('\n','<br />')
        txt = txt.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;')

        pg = Paragraph(txt, style)

        story.append(pg)