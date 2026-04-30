import json
import unittest
from io import TextIOWrapper

from scripts.list_missing_cards.python.src.Card import Card

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