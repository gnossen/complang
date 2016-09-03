import urllib.request
from bs4 import BeautifulSoup

USE_DATABASE = False

def download_page(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

class Word:
    def __init__(self, url, language):
        self.url = url
        self.language = language
        self.word = None
        self.ipa = None
        self.time = None

    def get_word(self, root):
        return root.find_all("h1", class_="firstHeading")[0].getText()

    def get_section_title(self, section):
        try:
            return section.findAll("span", class_="mw-headline")[0].getText()
        except:
            return None

    def get_proper_section_index(self, sections):
        for i, (title, section) in enumerate(sections):
            if title == self.language:
                return i

        raise Exception("No Spanish section found.")

    def get_sections(self, root):
        headers = root.findAll("h2")

        sections = []
        for header in headers:
            section_title = self.get_section_title(header)
            if section_title is not None:
                sections += [(section_title, header)]

        return sections

    def download(self):
        page = download_page(self.url)
        root = BeautifulSoup(page, "html.parser")
        self.word = self.get_word(root)
        sections = self.get_sections(root)

        # get proper tag after the section and before the subsequent section
        # in case Spanish is the final section, do different case
        print(sections)

    def archive(self):
        if USE_DATABASE:
            pass
        else:
            print(self)

    def __repr__(self):
        return "<Word: '%s', '%s'>" % (self.word, self.ipa)

    __str__ = __repr__

word = Word("https://en.wiktionary.org/wiki/ababillarse", "Spanish")
word.download()
word.archive()
