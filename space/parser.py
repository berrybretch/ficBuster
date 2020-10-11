from bs4 import BeautifulSoup


class Parser:
    def __init__(self, pages):
        """
        data:
    
        only need to get these once, anywhere
        {
        docAuthor:str
        docTitle:str  
        }

        threadmarks:[ str for str in list]
        story:
            post_id:post
        """
        self.data = {}
        self.data["story"] = {}
        self.data["threadmarks"] = []
        self.pages = pages
        self.parse_meta_info(self.pages[0])
        self.run()

    def parse_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        articles = soup.select("article.message")
        story = dict(
            zip(
                [i["data-content"] for i in articles],
                [j.select("div.bbWrapper")[0].text for j in articles],
            )
        )
        threadmarks = [i.select("span.threadmarkLabel")[0].text for i in articles]

        return story, threadmarks

    def parse_meta_info(self, html):
        soup = BeautifulSoup(html, "lxml")
        article = soup.select("article.message")
        self.data["docAuthor"] = article[0]["data-author"]
        self.data["docTitle"] = soup.select("title")[0].text

    def run(self):
        for i in self.pages:
            x = self.parse_html(i)
            self.data["story"] = dict(self.data["story"], **x[0])
            self.data["threadmarks"].extend(x[1])
        for k, v in self.data["story"].items():
            v = v.replace("<", "/~")
            v = v.replace(">", "~\\")

    def __repr__(self):
        temp = []
        for key, value in self.data["story"].items():
            temp.append(f"{key} : {len(value)}")
        return "\n".join(temp)

