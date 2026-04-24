import json
import unittest
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.Card import Card
from scripts.list_missing_cards.python.src.Exceptions.ParsingException import ParsingException
from scripts.list_missing_cards.python.src.Exceptions.ParameterException import ParameterException
from scripts.list_missing_cards.python.src.Exceptions.InvalidCSVBodyException import InvalidCSVBodyException


class InitCardTest(unittest.TestCase):
    def setUp(self):
        self.firstCard = Card(1, 1, 'H', 'EN', 0, 'Axiom', 'Sierra & Oddball')

    def tearDown(self):
        return super().tearDown()

    def test_init(self):
        self.assertIsInstance(self.firstCard, Card)

class TestFromCSV(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        hero_csv_absolute_path: str = datatest_dir_path+"oneHeroCard.csv"
        unit_csv_absolute_path: str = datatest_dir_path+"oneUnitCard.csv"
        self.heroFromCSVCard = Card.from_csv(hero_csv_absolute_path)
        self.unitFromCSVCard = Card.from_csv(unit_csv_absolute_path)

        config_file = open("../config.json")
        json_config = json.load(config_file)
        config_file.close()
        config_csv_location: dict = json_config['csv']['location']
        light_csv_absolute_path: str = (
                config_csv_location['parent_dir_absolute_path']+'/'+
                config_csv_location['filename']
        )

        self.cardsFromCSVFile = Card.from_csv(light_csv_absolute_path)

        #test with a wrong file path
        #test with a wrong formated file

    def tearDown(self):
        return super().tearDown()

    def test_instantiateAList(self):
        self.assertIsInstance(self.cardsFromCSVFile, list)

    def test_instantiateAListOfCards(self):
        for card in self.cardsFromCSVFile:
            self.assertIsInstance(card, Card)

    def test_instantiateHero(self):
        self.assertIsInstance(self.heroFromCSVCard[0], Card)
        self.assertEqual('H', self.heroFromCSVCard[0].codeType)

    def test_instantiateUnit(self):
        self.assertIsInstance(self.unitFromCSVCard[0], Card)
        self.assertIn(self.unitFromCSVCard[0].codeType, ['C','R','F'])

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

class TestParseCodeType(unittest.TestCase):
    def setUp(self):
        self.heroCase: str = Card.parse_code_type('H - Héro')
        self.out0fFactionCase: str = Card.parse_code_type('F - Transfuge')
        self.rareCase: str = Card.parse_code_type('R - Rare')
        self.commonCase: str = Card.parse_code_type('C - Commune')

    def test_returnString(self):
        self.assertIsInstance(self.heroCase, str)
        self.assertIsInstance(self.out0fFactionCase, str)
        self.assertIsInstance(self.rareCase, str)
        self.assertIsInstance(self.commonCase, str)

    def test_oneCharLength(self):
        self.assertEqual(1, len(self.heroCase))
        self.assertEqual(1, len(self.out0fFactionCase))
        self.assertEqual(1, len(self.rareCase))
        self.assertEqual(1, len(self.commonCase))

    def test_value(self):
        self.assertEqual('H', self.heroCase)
        self.assertEqual('F', self.out0fFactionCase)
        self.assertEqual('R', self.rareCase)
        self.assertEqual('C', self.commonCase)

class TestCSVToDictList(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        self.heroCSVFile = open(
            datatest_dir_path+"oneHeroCard.csv",
            'r', encoding='utf-8-sig'
        )
        self.heroList = Card.csv_to_dict_list(self.heroCSVFile)
    def tearDown(self):
        self.heroCSVFile.close()
        return super().tearDown()

    def test_returnAList(self):
        self.assertIsInstance(self.heroList, list)

    def test_returnAListOfDict(self):
        for item in self.heroList:
            self.assertIsInstance(item, dict)

class TestCSVHeaderValidation(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        self.heroCSVFile = open(
            datatest_dir_path+"oneHeroCard.csv",
            'r', encoding='utf-8-sig')
        self.wrongHeadersCSVFile = open(
            datatest_dir_path+"wrongHeaders.csv",
            'r', encoding='utf-8-sig')

    def tearDown(self):
        self.heroCSVFile.close()
        self.wrongHeadersCSVFile.close()
        return super().tearDown()

    def test_returnFileType(self):
        self.assertIsInstance(
            Card.csv_header_validation(self.heroCSVFile),
            TextIOWrapper
        )

    def test_withWrongHeaders(self):
        with self.assertRaises(ParsingException) as cm:
            Card.csv_header_validation(self.wrongHeadersCSVFile)
        wrong_headers_exception = cm.exception
        self.assertEqual(400, wrong_headers_exception.error_code)
        self.assertEqual(
            "Mauvais format CSV: une/des clés n'est pas présente de le header",
            wrong_headers_exception.message)

    def test_withGoodHeaders(self):
        self.assertTrue(Card.csv_header_validation(self.heroCSVFile))

class TestCSVBodyValidation(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        self.emptyBodyFile: TextIOWrapper = open(
            datatest_dir_path+"emptyBody.csv",
            'r', encoding='utf-8-sig'
        )

        self.properBodyFile: TextIOWrapper = open(
            datatest_dir_path+"oneHeroCard.csv",
            'r', encoding='utf-8-sig'
        )

    def tearDown(self):
        self.emptyBodyFile.close()
        self.properBodyFile.close()

    def test_returnFileType(self):
        self.assertIsInstance(
            Card.csv_body_validation(self.properBodyFile),
            TextIOWrapper
        )

    def test_emptyCSVBody(self):
        with self.assertRaises(InvalidCSVBodyException) as context:
            Card.csv_body_validation(self.emptyBodyFile)
        exception: InvalidCSVBodyException = context.exception
        self.assertEqual(
            f"This file is not properly filled at line 1, key 'ID'."
            f" Make sure to fill at least one line of content after the header.",
            exception.message
        )
class TestFindBodyCorruption(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        filled_body_file: TextIOWrapper = open(
            datatest_dir_path+"oneHeroCard.csv",
            'r', encoding='utf-8-sig'
        )

        empty_body_file: TextIOWrapper = open(
            datatest_dir_path+"emptyBody.csv",
            'r', encoding='utf-8-sig'
        )

        self.filledBodyResult: dict = Card.find_body_corruption(filled_body_file)
        self.emptyBodyResult: dict = Card.find_body_corruption(empty_body_file)

        filled_body_file.close()
        empty_body_file.close()

    def test_returnDict(self):
        self.assertIsInstance(
            self.filledBodyResult,
            dict
        )
        self.assertIsInstance(
            self.emptyBodyResult,
            dict
        )


    def test_returnDictKeys(self):
        self.assertIn('status', self.filledBodyResult)
        self.assertIn('status', self.emptyBodyResult)
        self.assertIn('line', self.emptyBodyResult)
        self.assertIn('key', self.emptyBodyResult)

    def test_DictKeysTypes(self):
        self.assertIsInstance(
            self.filledBodyResult['status'],
            bool
        )
        self.assertIsInstance(
            self.emptyBodyResult['status'],
            bool
        )
        self.assertIsInstance(
            self.emptyBodyResult['line'],
            int
        )
        self.assertIsInstance(
            self.emptyBodyResult['key'],
            str
        )

class TestIsBodyEmpty(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        self.emptyBodyFile: TextIOWrapper = open(
            datatest_dir_path+"emptyBody.csv",
            'r', encoding='utf-8-sig'
        )
        self.filledBodyFile: TextIOWrapper = open(
            datatest_dir_path + "oneHeroCard.csv",
            'r', encoding='utf-8-sig'
        )

    def tearDown(self):
        self.emptyBodyFile.close()
        self.filledBodyFile.close()

    def test_returnBool(self):
        self.assertIsInstance(
            Card.is_body_empty(self.emptyBodyFile),
            bool
        )

    def test_emptyBodyCase(self):
        self.assertTrue(Card.is_body_empty(self.emptyBodyFile))

    def test_filledBodyCase(self):
        self.assertFalse(Card.is_body_empty(self.filledBodyFile))