import unittest

from scripts.list_missing_cards.python.src.Card import Card

class InitCardTest(unittest.TestCase):
    def setUp(self):
        self.firstCard = Card(1, 1, 'H', 'EN', 0, 'Axiom', 'Sierra & Oddball')

    def tearDown(self):
        return super().tearDown()

    def test_init(self):
        self.assertIsInstance(self.firstCard, Card)

class TestFromCSVTest(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        self.heroCSVFile = open(datatest_dir_path+"oneHeroCard.csv", 'r')
        self.unitCSVFile = open(datatest_dir_path+"oneUnitCard.csv", 'r')
        self.heroFromCSVCard = Card.from_csv(self.heroCSVFile)
        self.unitFromCSVCard = Card.from_csv(self.unitCSVFile)
        #test with an empty file
        #test with a wrong formated file

        data_dir_path = "../../../../data/"
        self.lightFRCSVFile = open(data_dir_path+"csv/BTG_Collection-lightFR.csv", 'r')
        self.cardsFromCSVFile = Card.from_csv(self.lightFRCSVFile)

    def tearDown(self):
        self.heroCSVFile.close()
        self.unitCSVFile.close()
        self.lightFRCSVFile.close()
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

class TestCSVLineToDict(unittest.TestCase):
    def setUp(self):
        self.csv_lines: list[list[str]] = [
            ['ID', 'Code de Type', 'Langue', 'Nom', 'Faction', 'Type unité', 'Possession'],
            ['1', 'H - Héro', 'EN - English', 'Sierra & Oddball', 'Axiom', '', '0']
        ]
        self.dictHeroData: dict = Card.csv_line_to_dict(self.csv_lines[1])
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

class TestCSVToDictList(unittest.TestCase):
    def setUp(self):
        datatest_dir_path = "data/"
        self.heroCSVFile = open(datatest_dir_path+"oneHeroCard.csv", 'r')
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
        self.heroCSVFile = open(datatest_dir_path+"oneHeroCard.csv", 'r')
        self.wrongHeadersCSVFile = open(datatest_dir_path+"wrongHeaders.csv", 'r')

    def tearDown(self):
        self.heroCSVFile.close()
        self.wrongHeadersCSVFile.close()
        return super().tearDown()

    def test_returnBoolean(self):
        self.assertIsInstance(
            Card.csv_header_validation(self.heroCSVFile),
            bool
        )

    def test_withWrongHeaders(self):
        self.assertFalse(Card.csv_header_validation(self.wrongHeadersCSVFile))

    def test_withGoodHeaders(self):
        self.assertTrue(Card.csv_header_validation(self.heroCSVFile))