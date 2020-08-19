
from bs4 import BeautifulSoup
import requests
import threading
import pickle
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
import ebooklib
import pickle
import sys
###
sys.setrecursionlimit(50000)

class SpaceBattler:
    def __init__(self, link):
        self.link = link+'/reader' if 'reader' not in link else link
        self.ses = requests.Session()

    def find_links(self):
        #response test
        #link test?
        #return number of pages instead?
        response = self.ses.get(self.link)
        soup = BeautifulSoup(response.text, 'lxml')
        pages = soup.find_all('li', class_='pageNav-page')
        if len(pages) == 0:
            return 1
        else:
            number_of_links = int(pages[-1].string)
            return number_of_links

    def grab_content(self, page_number):
        response = self.ses.get(f'{self.link}/page-{page_number}')
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find_all('div', class_='bbWrapper')
        threads = soup.find_all('span', class_='threadmarkLabel')
        chapters = [i.string for i in threads]
        page = {k:v for k in chapters for v in content}
        return (page_number, page)

    def execution(self):
        number_of_links = self.find_links() + 1
        with ThreadPoolExecutor() as exec:
            futures = exec.map(self.grab_content, range(1, number_of_links))
        ans = list(futures)
        return ans



        #pass all pages in
        #yield pages joined to page number
        #return all pages in order?
        pass


    def epub_pack(self):
        pass




if __name__ == "__main__":
    onePageTest = "https://forums.spacebattles.com/threads/bastille-worm-hamefura.873739"
    severalPageTest= "https://forums.spacebattles.com/threads/compulsion-worm-prototype.821228"
    x =SpaceBattler("https://forums.spacebattles.com/threads/compulsion-worm-prototype.821228")
    y = x.find_links()
    z = x.execution()
    pickle.dump(z, open('sus', 'wb'))
    pprint(y)
