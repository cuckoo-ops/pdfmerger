import os
import unittest

from pdf_merger.main import list_pdf_directory, sort_pdf_files, merge_pdf

test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_data'))


class TestMain(unittest.TestCase):
    def test_merge(self):
        input_files = list_pdf_directory(test_data_dir)
        sorted_files = sort_pdf_files(input_files)
        merge_pdf(sorted_files, os.path.join(test_data_dir, 'test_out.pdf'), False)


if __name__ == '__main__':
    unittest.main()
