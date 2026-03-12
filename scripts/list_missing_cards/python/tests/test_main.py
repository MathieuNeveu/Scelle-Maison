import unittest

from scripts.list_missing_cards.python.src.main import ma_fonction

class TestHelloWorld(unittest.TestCase):

    def test_outputlength(self):
        self.assertEqual(len(ma_fonction()), len('Hello World'))

    def test_isHelloworld(self):
        self.assertEqual(ma_fonction(), 'Hello World')

if __name__ == '__main__':
    unittest.main()