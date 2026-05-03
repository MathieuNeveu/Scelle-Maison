import unittest

from scripts.list_missing_cards.python.src.CSV import CSV

class TestGetDataAsDict(unittest.TestCase):
    def setUp(self):
        self.csv_file: CSV = CSV()
        self.dict_data: dict = self.csv_file.get_data_as_dict()

    def test_return_dict(self):
        self.assertIsInstance(self.csv_file.get_data_as_dict(), dict)

    def test_return_an_header_key(self):
        self.assertIn('header', self.dict_data)

    def test_header_should_be_list(self):
        self.assertIsInstance(self.dict_data['header'], list)

    def test_return_a_body_key(self):
        self.assertIn('body', self.dict_data)
