import json
import unittest
from collections.abc import Callable
from unittest.mock import mock_open, patch

from scripts.list_missing_cards.python.src.File import File
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
            File.open_with_process(self.good_filepath, lambda filename: True)
        )

    def test_exception_with_wrong_filename(self):
        with self.assertRaises(FileNotFoundError):
            File.open_with_process(self.wrong_filepath, lambda filename: True)

    def test_wrong_file_path_type(self):
        wrong_parameter: int = 666
        with self.assertRaises(ParameterException) as context:
            File.open_with_process(wrong_parameter, lambda filename: True)
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

    def test_opens_file_in_read_mode(self):
        with patch('builtins.open', mock_open()) as mock_file:
            File.open_with_process('filename.txt', lambda filename: True)
            mock_file.assert_called_once_with('filename.txt', 'r')

    def test_processes_on_the_file(self):
        file_content:str = '54'
        def sum_file_values(file) -> int:
            content: str = file.read()
            return int(content[0]) + int(content[1])
        with patch('builtins.open', mock_open(read_data=file_content)):
            self.assertEqual(
                9,
                File.open_with_process(
                    'filename.txt',
                    sum_file_values
                )
            )

    def test_exception_when_passing_int_type_as_process(self):
        wrong_process: int = 666
        with self.assertRaises(ParameterException) as context:
            with patch('builtins.open', mock_open()):
                File.open_with_process('filename.txt', wrong_process)
        exception: ParameterException = context.exception
        self.assertEqual(400, exception.error_code)
        self.assertEqual(Callable, exception.expected_type)
        self.assertEqual(int, exception.parameter_type)
        self.assertEqual('process', exception.parameter_name)
        self.assertEqual('open_with_process', exception.method_name)
        self.assertEqual(
            "In `open_with_process` method, `process` parameter Exception (400)."
            " <class 'int'> type founded instead of <class 'collections.abc.Callable'>",
            exception.message
        )

    def test_exception_when_passing_str_type_as_process(self):
        wrong_process: str = '666'
        with self.assertRaises(ParameterException) as context:
            with patch('builtins.open', mock_open()):
                File.open_with_process('filename.txt', wrong_process)
        exception: ParameterException = context.exception
        self.assertEqual(400, exception.error_code)
        self.assertEqual(Callable, exception.expected_type)
        self.assertEqual(str, exception.parameter_type)
        self.assertEqual('process', exception.parameter_name)
        self.assertEqual('open_with_process', exception.method_name)
        self.assertEqual(
            "In `open_with_process` method, `process` parameter Exception (400)."
            " <class 'str'> type founded instead of <class 'collections.abc.Callable'>",
            exception.message
        )

class TestIsPathOk(unittest.TestCase):

    def test_should_be_boolean(self):
        self.assertIsInstance(File.is_path_ok('absolute_path'), bool)

    def test_int_arg_should_raise_parameter_exception(self):
        with self.assertRaises(ParameterException) as context:
            File.is_path_ok(6)
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

class TestIsProcessOk(unittest.TestCase):

    def test_should_be_boolean(self):
        self.assertIsInstance(File.is_process_ok(), bool)