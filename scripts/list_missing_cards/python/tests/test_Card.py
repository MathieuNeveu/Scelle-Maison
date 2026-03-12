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
        data_dir_path = "scripts/list_missing_cards/python/tests/data/"
        self.heroCSVFile = open(data_dir_path+"oneHeroCard.csv", 'r')
        self.unitCSVFile = open(data_dir_path+"oneUnitCard.csv", 'r')
        self.heroFromCSVCard = Card.from_csv(self.heroCSVFile)
        self.unitFromCSVCard = Card.from_csv(self.unitCSVFile)

    def tearDown(self):
        self.heroCSVFile.close()
        self.unitCSVFile.close()

    def test_instantiateHero(self):
        self.assertIsInstance(self.heroFromCSVCard, Card)