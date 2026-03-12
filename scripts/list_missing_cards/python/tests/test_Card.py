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

        data_dir_path = "../../../../data/"
        self.lightFRCSVFile = open(data_dir_path+"csv/BTG_Collection-lightFR.csv", 'r')
        self.cardsFromCSVFile = Card.from_csv(self.lightFRCSVFile)

    def tearDown(self):
        self.heroCSVFile.close()
        self.unitCSVFile.close()
        self.lightFRCSVFile.close()

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
        assert ['C','R','F'].__contains__(self.unitFromCSVCard[0].codeType)