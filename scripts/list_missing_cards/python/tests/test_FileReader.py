import json
import unittest

from scripts.list_missing_cards.python.src.FileReader import FileReader
from scripts.list_missing_cards.python.src.Exceptions.ParameterException import ParameterException

class TestOpenWithProcess(unittest.TestCase):
    def setUp(self):
        config_file = open("../config.json")
        json_config = json.load(config_file)
        config_file.close()

        self.config_csv_location: dict = json_config['csv']['location']
        self.good_filepath: str = (
                self.config_csv_location['parent_dir_absolute_path']+'/'+
                self.config_csv_location['filename']
        )

        self.wrong_filepath: str = (
                self.config_csv_location['parent_dir_absolute_path']+
                '/bad_name.csv'
        )

    def tearDown(self):
        return super().tearDown()

    def test_no_exception_with_good_filename(self):
        self.assertTrue(
            FileReader.open_with_process(self.good_filepath, lambda filename: True)
        )

    def test_exception_with_wrong_filename(self):
        with self.assertRaises(FileNotFoundError) as context:
            FileReader.open_with_process(self.wrong_filepath, lambda filename: True)

    def test_wrong_file_path_type(self):
        wrong_parameter: int = 666
        with self.assertRaises(ParameterException) as context:
            FileReader.open_with_process(wrong_parameter, lambda filename: True)
        exception: ParameterException = context.exception
        self.assertEqual(400, exception.error_code)
        self.assertEqual(str, exception.expected_type)
        self.assertEqual(int, exception.parameter_type)
        self.assertEqual('file_absolute_path', exception.parameter_name)
        self.assertEqual(
            "In `open_with_process` method, `file_absolute_path` parameter Exception (400)."
            " <class 'int'> type founded instead of <class 'str'>",
            exception.message
        )
