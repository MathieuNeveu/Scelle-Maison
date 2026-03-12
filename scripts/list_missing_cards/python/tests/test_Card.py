import unittest

from scripts.list_missing_cards.python.src.Card import Card

class InitCardTest(unittest.TestCase):
    def setUp(self):
        self.firstCard = Card(1, 1, 'H', 'EN', 0, 'Axiom', None)

    def tearDown(self):
        return super().tearDown()

    def test_init(self):
        self.assertIsInstance(self.firstCard, Card)

class TestFromCSVTest(unittest.TestCase):
    def setUp(self):
        self.heroCSVFile = open('data/oneHeroCard.csv')
        self.unitCSVFile = open('data/oneUnitCard.csv')
        self.heroFromCSVCard = Card.fromCSV(self.heroCSVFile)
        self.unitFromCSVCard = Card.fromCSV(self.unitCSVFile)

    def test_instantiateHero(self):
        self.assertIsInstance(self.heroCSVFile, Card)