import re
import time

import pdfplumber

from pdf_merger import ExtractPageIndexError
from decimal import Decimal


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
    index_on_line = -1
    index_pattern = r'(\d+)'
    on_top = True

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @classmethod
    def search_page_index(cls, page):
        text = page.extract_text().split('\n')
        index = re.findall(cls.index_pattern, text[cls.index_on_line])[0]
        return index

    def test_extract_pages_index(self, pages_count=2):
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_index in range(pages_count):
                page = pdf.pages[page_index]
                index = self.search_page_index(page)
                print(f'{page.page_number}: Real PageNumber {index}')

    def display_page_text(self, pages_count=2, line_count=5):
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_index in range(pages_count):
                page = pdf.page[page_index]
                text = page.extract_text().split('\n')
                rg = min(len(text), line_count)
                search_range = range(rg)
                for l in search_range:
                    print(f'{l} {text[l]}')

                search_range = range(-1, -rg, -1)
                for l in search_range:
                    print(f'{l} {text[l]}')

    def extract_pages_index(self) -> Pages:
        page_indexes = Pages()
        with pdfplumber.open(self.pdf_path) as pdf:
            try:
                for page in pdf.pages:
                    s = time.time()
                    index = self.search_page_index(page)
                    print(f'extract index: {time.time() - s}')
                    page_indexes.append(Page(self.pdf_path, int(index)))
            except Exception as e:
                raise ExtractPageIndexError(f'{index} on \'{self.pdf_path}\'', )
        return page_indexes
