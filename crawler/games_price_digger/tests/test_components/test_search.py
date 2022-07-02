import unittest
from games_price_digger.src.components import Search


class SearchTests(unittest.TestCase):

    def test_is_the_searched_game(self):
        """Test the game checking method"""
        search = Search('Tetris', 'Steam')
        game_to_check = 'tetris?'
        result = search.is_the_searched_game(game_to_check)
        self.assertTrue(result)

    def test_is_not_the_searched_game(self):
        """Test the game checking method with a not invalid game"""
        search = Search('Tetris', 'Steam')
        game_to_check = 'tetris 2'
        result = search.is_the_searched_game(game_to_check)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
