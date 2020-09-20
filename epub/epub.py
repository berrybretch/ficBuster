from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import tempfile
import uuid
import shutil

env = Environment(
    loader=FileSystemLoader("./templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
##should have three functions.
#create all the documentation in one function
#zip the docs up
#cleanup everything

class Epub:
    def __init__(self, data):
        """shape of scraper.data
            threadmarks: [list of threadmarks]
            lang: eng
            author:
            title:
            story: { post_id: string}
            uid:
        """
        self.data = data
        self.data["uid"] = str(uuid.uuid4())
        self.data["filename"] = [
            f'{i.replace(" ", "")}' for i in self.data["threadmarks"]
        ]
        self.data['oebps'] = ''
        self.data['meta_inf'] = ''


    def generate_ncx(self,location):
        template = env.get_template("ncx_template.ncx")
        template.stream(self.data).dump(f'{location}/toc.ncx')

    def generate_opf(self, location):
        template = env.get_template("opf_template.opf")
        template.stream(self.data).dump(f'{location}/content.opf')

    def generate_meta_inf(self, location):
        Template("data_template").dump(f"{location}/container.xml")
    

    def generate_chapters(self, location):
        template = env.get_template("chapter_template.xhtml")
        for index, key in self.data["story"]:
            template.stream(
                {
                    "threadmark": self.data["threadmarks"][index],
                    "content": self.data["story"][key],
                }
            ).dump(f'{location}/{self.data["filename"][index]}')


    def generate_title(self, location):
        template = env.get_template("title_template.xhtml")
        template.stream(self.data).dump(f'{location}/title.xhtml')

    def generate_css(self, location):
        env.get_template("page_css.css").stream().dump(f'{location}/page_style.css')
        env.get_template("stylesheet.css").stream().dump(f'{location}/stylesheet.css')

    def dir_constructor(self):
        with tempfile.TemporaryDirectory(dir='/tmp') as parent:

            #create nested directories
            oebps = tempfile.mkdtemp(dir=parent)
            meta_inf = tempfile.mkdtemp(dir=parent)

            #i need these paths for later
            self.data['oebps']+= oebps.split('/')[-1]
            self.data['meta_inf'] += meta_inf.split('/')[-1]

            #start dumping all docs
            self.generate_title(parent)
            self.generate_ncx(parent)
            self.generate_meta_inf(meta_inf)
            self.generate_opf(parent)
            self.generate_chapters(oebps)
            self.generate_css(parent)
            Template('application/epub+zip').stream().dump(f'{parent}/mimetype')
            #zip_it_all_together
            shutil.make_archive(self.data['title'], 'zip',parent)
    
            







        


            






        
