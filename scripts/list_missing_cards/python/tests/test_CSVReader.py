import json
import unittest
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.Card import Card
from scripts.list_missing_cards.python.src.Exceptions.ParameterException import ParameterException

class TestOpenCSVFile(unittest.TestCase):
    def setUp(self):
        config_file = open("../config.json")
        json_config = json.load(config_file)
        config_file.close()

        self.config_csv_location: dict = json_config['csv']['location']
        good_filepath: str = (
                self.config_csv_location['parent_dir_absolute_path']+'/'+
                self.config_csv_location['filename']
        )

        self.wrong_filepath: str = (
                self.config_csv_location['parent_dir_absolute_path']+
                '/bad_name.csv'
        )

    def tearDown(self):
        return super().tearDown()

    def test_wrongPathType(self):
        wrong_parameter: TextIOWrapper = open('../config.json')
        with self.assertRaises(ParameterException) as context:
            Card.open_csv_file(wrong_parameter)
        exception: ParameterException = context.exception
        self.assertEqual(400, exception.error_code)
        self.assertEqual(str, exception.expected_type)
        self.assertEqual(TextIOWrapper, exception.parameter_type)
        self.assertEqual('csv_absolute_path', exception.parameter_name)
        self.assertEqual(
            "In `open_csv_file` method, `csv_absolute_path` parameter Exception (400)."
            " <class '_io.TextIOWrapper'> type founded instead of <class 'str'>",
            exception.message
        )

    def test_wrongFileName(self):
        with self.assertRaises(FileNotFoundError) as context:
            Card.open_csv_file(self.wrong_filepath)
        exception: FileNotFoundError = context.exception
        self.assertIn(
            self.config_csv_location['parent_dir_absolute_path'],
            str(exception)
        )

class TestCSVLineToDict(unittest.TestCase):
    def setUp(self):
        self.csv_lines: list[list[str]] = [
            ['1', 'H - Héro', 'EN - English', 'Sierra & Oddball', 'Axiom', '', '0'],
            ['0', 'X', 'YY - English', 'Sierra & Oddball', 'Axiom', '', '0']
        ]
        self.dictHeroData: dict = Card.csv_line_to_dict(self.csv_lines[0])
    def tearDown(self):
        return super().tearDown()

    def test_returnDict(self):
        self.assertIsInstance(self.dictHeroData, dict)

    def test_idInDict(self):
        self.assertIn("_id", self.dictHeroData)

    def test_indexInDict(self):
        self.assertIn("index", self.dictHeroData)

    def test_codeTypeInDict(self):
        self.assertIn("codeType", self.dictHeroData)

    def test_langInDict(self):
        self.assertIn("lang", self.dictHeroData)

    def test_unitsInDict(self):
        self.assertIn("units", self.dictHeroData)

    def test_factionInDict(self):
        self.assertIn("faction", self.dictHeroData)

    def test_nameInDict(self):
        self.assertIn("name", self.dictHeroData)

    def test_returnExpectedCodeType(self):
        expected: str = 'H'
        self.assertEqual(expected, self.dictHeroData['codeType'])

