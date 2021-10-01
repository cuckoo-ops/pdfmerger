import pdfplumber

from pdf_merger import ExtractPageIndexError


class Page():
    def __init__(self, path, index):
        self.path = path
        self.index = index

    def __hash__(self):
        return hash(self.index)

    def __eq__(self, other):
        return self.index == other.index


class Pages():
    def __init__(self):
        self.pages = []
        self.unique_pages = []

    def sort(self):
        self.unique_pages = list(dict.fromkeys(self.pages))
        self.unique_pages.sort(key=lambda x: x.index)

    def has_duplicate(self):
        return len(self.unique_pages) < len(self.pages)

    def append(self, page: Page):
        self.pages.append(page)

    def extend(self, pages):
        self.pages.extend(pages.pages)

    def get_path_indexes(self):
        if len(self.unique_pages) == 0: return
        before_page = self.unique_pages[0]
        path_index = [(before_page.path, [before_page.index])]
        for page in self.unique_pages[1:]:
            if page.path != before_page.path:
                path_index.append((page.path, []))
            path_index[-1][1].append(page.index)
            before_page = page
        return path_index


class Pdf(object):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_pages_index(self) -> Pages:
        page_indexes = Pages()
        with pdfplumber.open(self.pdf_path) as pdf:
            try:
                for page in pdf.pages:
                    # index = page.extract_words()[-1]['text']
                    text = page.extract_text()
                    index = text.splitlines()[-1].strip()
                    page_indexes.append(Page(self.pdf_path, int(index)))
            except Exception as e:
                raise ExtractPageIndexError(f'{index} on \'{self.pdf_path}\'', )
        return page_indexes
