from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import tempfile
import shutil
import os
import pickle

##should have three functions.
# create all the documentation in one function
# zip the docs up
# cleanup everything
"""

folder_structure should be this 
Book
    ++META_INF
        -container.xml
    ++OEBPS
        -filename.xhtml ##chapters
    -content.opf
    -mimetype
    -page_styles.css *
    -stylesheet.css *
    -titlepage.xhtml*
    -toc.ncx*

"""


class Epub:
    def __init__(self, data):
        self.data = data
        self.data["filenames"] = [key for key in self.data["story"].keys()]
        pl = FileSystemLoader("./templates")
        self.env = Environment(loader=pl, autoescape=select_autoescape(["html", "xml"]))
        self.parent = ''
        self.clean_data_kidogo()

    def clean_data_kidogo(self):
        #should be in space.py
        for key in self.data['story'].keys():
            self.data['story'][key] = self.data['story'][key].replace('<', '/~')
            self.data['story'][key] = self.data['story'][key].replace('>', '~\\')




    def construct(self):
        # setting up directories here
        parent = tempfile.mkdtemp()
        oebps = tempfile.mkdtemp(dir=parent)
        meta_inf = tempfile.mkdtemp(dir=parent)
        
        os.rename(meta_inf, f'{parent}/META-INF')
        meta_inf.replace(meta_inf.split('/')[-1], 'META-INF')

        self.data["oebps"] = oebps.split("/")[-1]
        self.data["meta_inf"] = 'META-INF'

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
            f"{parent}/META-INF/container.xml"
        )
        self.env.get_template('mimetype').stream().dump(
            f"{parent}/mimetype"
        )
        for index, filename in enumerate(self.data["filenames"]):
            self.env.get_template("chapter_template.xhtml").stream(
                threadmark=self.data["threadmarks"][index],
                content=self.data["story"][filename],
            ).dump(f"{oebps}/{self.data['filenames'][index]}.xhtml")
        self.parent = parent

    @staticmethod
    def zipper(name, path):
        return shutil.make_archive(name, 'zip',path)



if __name__ == "__main__":
    x = pickle.load(open('../data.pickle', 'rb'))
    cheese = Epub(x)
    cheese.construct()
    zip = cheese.zipper('example', cheese.parent)