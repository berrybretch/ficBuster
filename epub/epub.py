from jinja2 import Environment, FileSystemLoader, select_autoescape
from bs4 import BeautifulSoup, SoupStrainer

env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def _parse_soup(html):
        '''
        Grab all the good stuff from the response.
        good_stuff is 
        '''
        print("Straining")
        strainer = SoupStrainer(
            attrs={
                "class": "message",
            }
        )
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.select('article.message')
        title = soup.select('title')[0].text
        
        document = {
            "uid":1010101,
            "docAuthor": articles[0]["data-author"],
            "docTitle":title,
            "index":[i for i, _ in enumerate(articles)],#temporary fix just to get it to work
            "depth":len(articles),
            "post_id": [i['data-content'] for i in articles],
            "threadmarks": [i.select('span.threadmarkLabel')[0].text for i in articles],
            "content":[i.select('div.bbWrapper')[0].text for i in articles],
        }
        return document








def generate_ncx(document):
    '''
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
    
    '''
    template = env.get_template('ncx_template.ncx')
    template.stream(document).dump('toc.ncx')

    



    
    
if __name__ == "__main__":
    with open('spacebattles.html', 'r') as html:
        doc = _parse_soup(html)
        generate_ncx(doc)
        