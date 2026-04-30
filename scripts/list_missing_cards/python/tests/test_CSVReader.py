import unittest
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.Card import Card
from scripts.list_missing_cards.python.src.Exceptions.ParsingException import ParsingException
from scripts.list_missing_cards.python.src.Exceptions.InvalidCSVBodyException import InvalidCSVBodyException

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
