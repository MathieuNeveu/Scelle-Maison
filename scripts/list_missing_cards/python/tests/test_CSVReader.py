import unittest

from scripts.list_missing_cards.python.src.CSV import CSV

class TestGetData(unittest.TestCase):

    def test_return_dict(self):
        self.assertIsInstance(CSV.get_data(), dict)

