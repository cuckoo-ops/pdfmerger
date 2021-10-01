import os
import unittest

from pdf_merger.main import list_pdf_directory, sort_pdf_files

test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_data'))

test_data_dir = 'F:\gitrepo\mfd\papers\.tmp-BOOK\\2020\\02'


class TestMain(unittest.TestCase):
    def test_pages_sort(self):
        input_files = list_pdf_directory(test_data_dir)
        sorted_files, has_duplicate = sort_pdf_files(input_files)
        print(sorted_files)


if __name__ == '__main__':
    unittest.main()
