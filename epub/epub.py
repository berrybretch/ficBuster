from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import os
import uuid

env = Environment(
    loader=FileSystemLoader("./templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class Epub:
    def __init__(self, document):
        self.document = document
        self.document["uid"] = uuid.uuid4()

    @staticmethod
    def generate_ncx(document):
        """
        Generates .ncx file from template in templates folder

        params:
            document:dict
        returns:
            None
        
        """
        document["filename"] = [
            f'{document["threadmarks"][index]}.xhtml' for index in document["index"]
        ]
        template = env.get_template("ncx_template.ncx")
        template.stream(document).dump("toc.ncx")

    @staticmethod
    def generate_opf(document):
        """
        generates opf document from content inside document

        params:

            
            
        """
        x = [i.replace(" ", "") for i in document["threadmarks"]]
        document["threadmarks"] = x
        template = env.get_template("opf_template.opf")
        template.stream(document).dump("content.opf")

    @staticmethod
    def generate_meta_inf():
        """
        Generates generic metainfo document.
        params:
            none
        returns:
            none
        """
        Template('meta_template').dump(
            "container.xml"
        )

    @staticmethod
    def generate_chapters(document):
        """
        Generates chapters from content inside dict
        params:
            document
        """
        template = env.get_template("chapter_template.xhtml")
        for index in document["index"]:
            filename = f'{document["threadmarks"][index]}.xhtml'
            template.stream(
                {
                    "threadmarkLabel": document["threadmarks"][index],
                    "content": document["content"][index],
                }
            ).dump(filename)
