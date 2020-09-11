from ebooklib import epub


#grab threadmark. grab chapter content
#add minimal css
#wrap?


class Novel:
    def __init__(
        self,
        identifier,
        title,
        language,
        author,
    ):
        self.book = epub.EpubBook()
        self.book.set_identifier(identifier)
        self.book.set_title(title)
        self.book.set_language(language)
        self.book.add_author(author)
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

    def chapters(
        self,
        chapters,
    ):
        for key in chapters.keys():
            chap = epub.EpubHtml(
                title=key,
                file_name=f"{key}.xhtml",
                lang='en'
            )
            chap.set_content(chapters[key])
            self.book.add_item(chap)
        
