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
