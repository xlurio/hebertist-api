import unittest
from unittest.mock import MagicMock
from games_price_digger.src.components.search import Search
from games_price_digger.src.lists import SearchGameList

search = MagicMock(spec=Search)


class SearchGameListTests(unittest.TestCase):

    def test_throw_on_invalid_add(self):
        """Test error handling when an invalid item is added to the list"""
        search.is_the_searched_game.return_value = False
        search_game_list = SearchGameList(search)
        with self.assertRaises(Exception):
            search_game_list.add_item('wrong')


if __name__ == '__main__':
    unittest.main()
