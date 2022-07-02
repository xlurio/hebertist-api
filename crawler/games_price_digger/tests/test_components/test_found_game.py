from cgitb import reset
import unittest
from games_price_digger.src.components import FoundGame


class FoundGameTests(unittest.TestCase):

    def test_get_name(self):
        """Test name getter"""
        payload = {
            'name': 'Tetris',
            'price': 2.99,
            'link': 'https://store.steam.com/tetris/',
        }
        game = FoundGame(**payload)
        result = game.get_name()
        self.assertEqual(result, payload['name'])

    def test_get_price(self):
        """Test price getter"""
        payload = {
            'name': 'Tetris',
            'price': 2.99,
            'link': 'https://store.steam.com/tetris/',
        }
        game = FoundGame(**payload)
        result = game.get_price()
        self.assertEqual(result, payload['price'])

    def test_get_link(self):
        """Test link getter"""
        payload = {
            'name': 'Tetris',
            'price': 2.99,
            'link': 'https://store.steam.com/tetris/',
        }
        game = FoundGame(**payload)
        result = game.get_link()
        self.assertEqual(result, payload['link'])

    def test_get_data(self):
        """Test full data getter"""
        expected_result = {
            'name': 'Tetris',
            'price': 2.99,
            'link': 'https://store.steam.com/tetris/',
        }
        game = FoundGame(**expected_result)
        result = game.get_data()
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
