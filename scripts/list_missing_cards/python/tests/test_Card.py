import unittest

from src.Card import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        self.firstCard = Card(1, 1, 'H', 'EN', 0, 'Axiom', None)

    def tearDown(self):
        return super().tearDown()

    def test_init(self):
        self.assertIsInstance(self.firstCard, Card)