import re
import pdfplumber
from pdf_merger import ExtractPageIndexError


class Page():
    def __init__(self, path, index, number):
        self.path = path
        self.index = index
        self.page_number = number

    def __hash__(self):
        return hash(self.page_number)

    def __eq__(self, other):
        return self.page_number == other.page_number


class Pages():
    def __init__(self):
        self.pages = []
        self.unique_pages = []

    def sort(self):
        self.unique_pages = list(dict.fromkeys(self.pages))
        self.unique_pages.sort(key=lambda x: x.page_number)

    def has_duplicate(self):
        return len(self.unique_pages) < len(self.pages)

    def append(self, page: Page):
        self.pages.append(page)

    def extend(self, pages):
        self.pages.extend(pages.pages)

    def get_path_indexes(self):
        '''

        :return: [(path, [(index, page_number),(index, page_number)]),]
        '''
        if len(self.unique_pages) == 0: return
        before_page = self.unique_pages[0]
        path_index = [(before_page.path, [(before_page.index, before_page.page_number)])]
        for page in self.unique_pages[1:]:
            if page.path != before_page.path:
                path_index.append((page.path, []))
            path_index[-1][1].append((page.index, page.page_number))
            before_page = page
        return path_index


class Pdf(object):
    line_numbers = [-1]
    pattern = r'(\d+)'

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def search_page_index(self, page, index_on_line, pattern):
        text = page.extract_text().split('\n')
        _index_on_line = min(index_on_line, len(text))
        try:
            index = re.findall(pattern, text[_index_on_line])[0]
            return int(index)
        except Exception:
            raise ExtractPageIndexError(
                f'Not found page number in line {_index_on_line} with pattern \'{pattern}\'\n{text[_index_on_line]}')

    def test_extract_pages_index(self, line_numbers: list, pattern, pages_count=2):
        with pdfplumber.open(self.pdf_path) as pdf:
            _pages_count = min(pages_count, len(pdf.pages))
            for page_index in range(_pages_count):
                page = pdf.pages[page_index]
                line_no = line_numbers[page_index % len(line_numbers)]
                index = self.search_page_index(page, line_no, pattern)
                print(f'{page.page_number-1}: PageNumber {index}')

    def display_page_text(self, pages_count=2, line_count=5):
        with pdfplumber.open(self.pdf_path) as pdf:
            print(f'total pages: {len(pdf.pages)}')
            _pages_count = min(pages_count, len(pdf.pages))
            for page_index in range(_pages_count):
                page = pdf.pages[page_index]
                text = page.extract_text().split('\n')
                rg = min(len(text), line_count)
                search_range = range(rg)
                for l in search_range:
                    print(f'<{l}> {text[l]}')
                print('...')
                search_range = range(-rg, 0, 1)
                for l in search_range:
                    print(f'<{l}> {text[l]}')
                print('\n')

    def extract_pages_index(self) -> Pages:
        page_indexes = Pages()
        with pdfplumber.open(self.pdf_path) as pdf:
            try:
                for page in pdf.pages:
                    index = page.page_number-1
                    line_no = self.line_numbers[index % len(self.line_numbers)]
                    number = self.search_page_index(page, line_no, self.pattern)
                    page_indexes.append(Page(self.pdf_path, index, number))
            except Exception:
                raise ExtractPageIndexError(f'{index} on \'{self.pdf_path}\'')
        return page_indexes
