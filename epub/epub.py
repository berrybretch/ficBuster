from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import os
import uuid

env = Environment(
    loader=FileSystemLoader("./templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class Epub:
    def __init__(self, meta):
        """shape of scraper.meta
            threadmarks: [list of threadmarks]
            lang: eng
            author:
            title:
            story: { post_id: string}
            uid:
            filenames: []

        """
        self.meta = meta
        self.meta["uid"] = uuid.uuid4()
        # todo self.meta['depth']
        self.meta["filename"] = [
            f'{i.replace(" ", "")}' for i in self.meta["threadmarks"]
        ]

    @staticmethod
    def generate_ncx(meta):
        """
        Generates .ncx file from template in templates folder

        params:
            document:dict
        returns:
            None
        
        """
        template = env.get_template("ncx_template.ncx")
        template.stream(meta)

    @staticmethod
    def generate_opf(meta):
        """
        generates opf document from content inside document

        params:

        """
        template = env.get_template("opf_template.opf")
        template.stream(meta)

    def generate_meta_inf(self):
        Template("meta_template").dump("container.xml")

    @staticmethod
    def generate_chapters(meta):
        template = env.get_template("chapter_template.xhtml")
        for index, key in meta["story"]:
            template.stream(
                {
                    "threadmark": meta["threadmarks"][index],
                    "content": meta["story"][key],
                }
            ).dump(meta["filename"][index])

    @staticmethod
    def generate_title(meta):
        template = env.get_template("title_template.xhtml")
        template.stream(meta)
