import os
import unittest
from pdf_merger.pdf import Pdf
from . import test_data_dir


class TestPdf(unittest.TestCase):
    def test_pdf_page_index(self):
        # pdf = Pdf(os.path.join(test_data_dir, '2003.07932v1.pdf'))
        pdf = Pdf(os.path.join(test_data_dir, '3.pdf'))
        # pdf.get_text()
        pdf.to_text()

if __name__ == '__main__':
    unittest.main()
