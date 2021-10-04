import os
import unittest

from pdf_merger.pdf import Pdf
from . import test_data_dir
from pdf_merger.pdf import Pages, Page


class TestPdf(unittest.TestCase):
    def test_search_page_index(self):
        pdf_path = os.path.join(test_data_dir, '3.pdf')
        pdf = Pdf(pdf_path)
        pages = pdf.extract_pages_index()
        self.assertTrue(isinstance(pages, Pages))
        self.assertEqual(len(pages.pages), 3)
        self.assertEqual(pages.pages[0].index, 25)
        self.assertEqual(pages.pages[1].index, 26)
        self.assertEqual(pages.pages[2].index, 27)

    def test_display_page_text(self):
        pdf_path = os.path.join(test_data_dir, '3.pdf')
        pdf = Pdf(pdf_path)
        pdf.display_page_text()

    def test_pages_get_path_indexes(self):
        pages = Pages()
        pages.append(Page('./11.pdf', 0,1))
        pages.append(Page('./11.pdf', 1,3))
        pages.append(Page('./11.pdf', 2,2))
        pages.append(Page('./11.pdf', 3,4))
        pages.append(Page('./11.pdf', 4,7))

        pages.append(Page('./2.pdf', 5, 5))
        pages.append(Page('./2.pdf', 6, 6))
        pages.append(Page('./2.pdf', 7, 7))
        pages.append(Page('./2.pdf', 8, 4))
        pages.sort()
        index = pages.get_path_indexes()
        self.assertTrue(pages.has_duplicate())
        self.assertEqual(len(index), 3)
        self.assertEqual(len(index[0][1]),4)
        self.assertEqual(len(index[1][1]),2)
        self.assertEqual(len(index[2][1]),1)


if __name__ == '__main__':
    unittest.main()
