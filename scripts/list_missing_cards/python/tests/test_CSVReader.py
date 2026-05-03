import unittest

from scripts.list_missing_cards.python.src.CSVReader import CSVReader

class TestGetData(unittest.TestCase):

    def test_return_dict(self):
        self.assertIsInstance(CSVReader.get_data(), dict)

