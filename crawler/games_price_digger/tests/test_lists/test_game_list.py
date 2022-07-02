import unittest
from unittest.mock import MagicMock
from games_price_digger.src.components.found_game import FoundGame
from games_price_digger.src.iterators.simple_iterator import SimpleIterator
from games_price_digger.src.lists import GameList

game_box1 = MagicMock(spec=FoundGame)
game_box2 = MagicMock(spec=FoundGame)
game_box3 = MagicMock(spec=FoundGame)


class GameBoxListTests(unittest.TestCase):

    def test_make_iterator(self):
        """test description"""
        game_list = GameList(game_box1, game_box2, game_box3)
        iterator = game_list.make_iterator()
        self.assertTrue(isinstance(iterator, SimpleIterator))


if __name__ == '__main__':
    unittest.main()
