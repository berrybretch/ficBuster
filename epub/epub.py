from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import tempfile
import os
import uuid
import pickle
import zipfile

##should have three functions.
# create all the documentation in one function
# zip the docs up
# cleanup everything

"""
zip it but do not compress because mimetype needs to not be compressed
"""


class Epub:
    def __init__(self, data):
        self.data = data
        self.data["filenames"] = [key for key in self.data["story"].keys()]
        self.data["oebps"] = ""
        self.data["meta_inf"] = ""
        self.data["uid"] = uuid.uuid4()
        pl = FileSystemLoader("./templates")
        self.env = Environment(loader=pl, autoescape=select_autoescape(["html", "xml"]))
        self.parent = ""
        self.construct()

    def construct(self):
        # setting up directories here
        parent = tempfile.mkdtemp()
        oebps = tempfile.mkdtemp(dir=parent)
        meta_inf = tempfile.mkdtemp(dir=parent)
        os.rename(meta_inf, f"{parent}/META-INF")
        meta_inf.replace(meta_inf.split("/")[-1], "META-INF")
        self.data["oebps"] = oebps.split("/")[-1]
        self.data["meta_inf"] = "META-INF"
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
        self.env.get_template("mimetype").stream().dump(f"{parent}/mimetype")
        for index, filename in enumerate(self.data["filenames"]):
            self.env.get_template("chapter_template.xhtml").stream(
                threadmark=self.data["threadmarks"][index],
                content=self.data["story"][filename],
            ).dump(f"{oebps}/{self.data['filenames'][index]}.xhtml")
        self.parent = parent

    @staticmethod
    def zipper(name, path):
        try:
            zip = zipfile.ZipFile(
                f"/tmp/{name}.epub", mode="x", compression=zipfile.ZIP_STORED
            )
            os.chdir(path)
            for root, dirs, files in os.walk("."):
                for file in files:
                    zip.write(os.path.join(root, file))
        except FileExistsError as e:
            print(e)
            print("The zip already exists")
        except Exception as e:
            print("any other error")
            print(e)
        finally:
            zip.close()
