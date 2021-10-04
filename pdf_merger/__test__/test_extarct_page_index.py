import os
import unittest

import pdfplumber

from pdf_merger.pdf import Pdf
from . import test_data_dir
from pdf_merger.pdf import Pages, Page

test_data_dir = 'F:\gitrepo\mfd\papers\.tmp-BOOK\\2020\\02'


class TestPdf(unittest.TestCase):
    def test_pdf_page_index(self):
        # pdf = Pdf(os.path.join(test_data_dir, '2003.07932v1.pdf'))
        pdf = Pdf(os.path.join(test_data_dir, '3.pdf'))
        # pdf.get_text()
        pdf.extract_pages_index()

    def test_pages_sort(self):
        pdf = Pdf(os.path.join(test_data_dir, '7.pdf'))
        pages = pdf.extract_pages_index()
        pages.sort()
        print(pages.get_path_indexes())
        self.assertFalse(pages.has_duplicate())

    def test_search_index(self):
        pdf_path = os.path.join(test_data_dir, '7.pdf')
        with pdfplumber.open(pdf_path) as pdf:
            index = Pdf.search_page_index(pdf.pages[0])
            print(index)

    def test_test_search_index(self):
        pdf_path = os.path.join(test_data_dir, '7.pdf')
        pdf = Pdf(pdf_path)
        pdf.test_extract_pages_index()

    def test_pages_get_path_indexes(self):
        pages = Pages()
        pages.append(Page('./11.pdf', 1))
        pages.append(Page('./11.pdf', 3))
        pages.append(Page('./11.pdf', 2))
        pages.append(Page('./11.pdf', 4))
        pages.append(Page('./11.pdf', 7))

        pages.append(Page('./2.pdf', 5))
        pages.append(Page('./2.pdf', 6))
        pages.append(Page('./2.pdf', 7))
        pages.append(Page('./2.pdf', 4))
        pages.sort()
        index = pages.get_path_indexes()
        self.assertEqual(len(index), 3)


if __name__ == '__main__':
    unittest.main()
