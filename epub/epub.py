from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import epub
import tempfile
import shutil
import pickle

##should have three functions.
# create all the documentation in one function
# zip the docs up
# cleanup everything
"""
the shape of the data is assuredly this 
{
    docTitle: str
    docAuthor: str
    uid: str
    filename: str
    threadmarks: list
    story: dict
    lang: str
    meta_inf: str
    oebps: str
}
folder_structure should be this 
Book
    ++META_INF
        -container.xml
    ++OEBPS
        -filename.xhtml ##chapters
        -image.jpg ##all images
    -content.opf
    -mimetype
    -page_styles.css *
    -stylesheet.css *
    -titlepage.xhtml*
    -toc.ncx*

#create filenames from threadmarks
#create environment for jinja2
#need to construct system as if you were reading 
#grab and dump templates based on the files above using tempfiles
#zip the tempdirectory and deliver somewhere
#destroy the tempfile.

"""


class Epub:
    def __init__(self, data):
        self.data = data
        self.data["filenames"] = [key for key in self.data["story"].keys()]
        pl = FileSystemLoader("./templates")
        self.env = Environment(loader=pl, autoescape=select_autoescape(["html", "xml"]))

    def construct(self):
        # setting up directories here
        parent = tempfile.mkdtemp()
        oebps = tempfile.mkdtemp(dir=parent)
        meta_inf = tempfile.mkdtemp(dir=parent)
        self.data["oebps"] = oebps.split("/")[-1]
        self.data["meta_inf"] = meta_inf.split("/")[-1]

        # dumping files here
        self.env.get_template("page_css.css").stream(data=self.data).dump(
            f"{parent}/page_styles.css"
        )
        self.env.get_template("stylesheet.css").stream(data=self.data).dump(
            f"{parent}/stylesheet.css"
        )
        self.env.get_template("title_template.xhtml").stream(data=self.data).dump(
            f"{parent}/titlepage.xhtml"
        )
        self.env.get_template("ncx_template.ncx").stream(data=self.data).dump(
            f"{parent}/toc.ncx"
        )
        self.env.get_template("opf_template.opf").stream(data=self.data).dump(
            f"{parent}/content.opf"
        )
        self.env.get_template("meta_template").stream().dump(
            f"{meta_inf}/container.xml"
        )
        for index, filename in enumerate(self.data["filenames"]):
            self.env.get_template("chapter_template.xhtml").stream(
                threadmark=self.data["threadmarks"][index],
                content=self.data["story"][filename],
            ).dump(f"{oebps}/{self.data['filenames'][index]}.xhtml")
        self.parent = parent
