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
    index_in_line = -1
    index_box = None
    index_pattern = r'\d+'

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @classmethod
    def extract_page_index(cls, text):
        return  re.match(cls.index_pattern, text)

    @classmethod
    def search_page_index(cls, page, pattern, rate=0.1):

        try:
            s = time.time()
            w = page.width
            h = page.height
            print(page.bbox)
            # Crop pages
            top_bbox = (Decimal.from_float(0), Decimal.from_float(0),
                        w, h * Decimal.from_float(rate))
            bottom_bbox = (Decimal.from_float(0),   h * Decimal.from_float(1 - rate),
                           w, h)
            page_crop = page.within_bbox(bbox=top_bbox,relative=True)

            text = page_crop.extract_words()
            print(text)
            text = text[-1]['text']
            matched_text = re.match(pattern, text)
            print(f'extract index: {time.time() - s}')
            if matched_text:
                cls.index_box = top_bbox
                cls.index_pattern = pattern
                return True
            else:
                cls.search_page_index(page, pattern, bottom_bbox)
        except Exception as e:
            print(e)

    def extract_pages_index(self) -> Pages:
        # import time
        page_indexes = Pages()
        # s = time.time()
        # crop_coords = [0, 0, x1, bottom]
        with pdfplumber.open(self.pdf_path) as pdf:
            try:
                # print(f'open file: {time.time()-s}')

                for page in pdf.pages:
                    s = time.time()
                    w = page.width
                    h = page.height

                    # Crop pages
                    my_bbox = (0, h * 0.5,
                               w, h * 0.5)
                    page_crop = page.crop(bbox=my_bbox)
                    index = page_crop.extract_words()[-1]['text']
                    # index = page.extract_words()[-1]['text']

                    # text = page.extract_text()
                    # index = text.splitlines()[self.index_in_line].strip()

                    print(f'extract index: {time.time() - s}')

                    page_indexes.append(Page(self.pdf_path, int(index)))

            except Exception as e:
                raise ExtractPageIndexError(f'{index} on \'{self.pdf_path}\'', )
        return page_indexes
