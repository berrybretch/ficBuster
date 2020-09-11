from jinja2 import Environment, FileSystemLoader, select_autoescape
from bs4 import BeautifulSoup, SoupStrainer

env = Environment(
    loader=FileSystemLoader("./templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


container_xml = """
<?xml version="1.0" encoding="UTF-8" ?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>

"""


def _parse_soup(html):
    """
        Grab all the good stuff from the response.
        good_stuff is 
        """
    print("Straining")
    strainer = SoupStrainer(attrs={"class": "message",})
    soup = BeautifulSoup(html, "lxml")
    articles = soup.select("article.message")
    title = soup.select("title")[0].text
    lang = soup.find("html")["lang"]

    document = {
        "lang": lang,
        "uid": 1010101,  # todo generate uuid
        "docAuthor": articles[0]["data-author"],
        "docTitle": title,
        "index": [
            i for i, _ in enumerate(articles)
        ],  # temporary fix just to get it to work
        "depth": len(articles),
        "post_id": [i["data-content"] for i in articles],
        "threadmarks": [i.select("span.threadmarkLabel")[0].text for i in articles],
        "content": [i.select("div.bbWrapper")[0].text for i in articles],
    }
    return soup


def generate_ncx(document):
    """
    Generates .ncx file from template in templates folder

    params:
        uid:integer
        length:integer len(post_id)
        document:dictionary
            structure of document
            {
                post_id:[]
                threadmark_labels:[]
                content:[]
            }
    returns:
        None
    
    """
    template = env.get_template("ncx_template.ncx")
    template.stream(document).dump("toc.ncx")


def generate_opf(document):
    """
    generates opf document

    params:
        docTitle:string
        lang:string
        identifier:string url
        docAuthor:string
        file_name:thread and content
            thread is ref.xhtml
            content is streamed to file
        
    """
    x = [i.replace(" ", "") for i in document["threadmarks"]]
    document["threadmarks"] = x
    template = env.get_template("opf_template.opf")
    template.stream(document).dump("content.opf")


def generate_chapter(documents):
    pass
