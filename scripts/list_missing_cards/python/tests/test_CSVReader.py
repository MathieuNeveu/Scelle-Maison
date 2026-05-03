import unittest

from scripts.list_missing_cards.python.src.CSV import CSV

class TestGetDataAsDict(unittest.TestCase):
    def setUp(self):
        self.csv_file: CSV = CSV()

    def test_return_dict(self):
        self.assertIsInstance(self.csv_file.get_data_as_dict(), dict)

