import unittest
from games_price_digger.src.lists.meta_game_list import MetaGameList


class MetaGameListTests(unittest.TestCase):

    def test_throw_error_on_invalid_item(self):
        """Test if a error is thrown when a invalid item is added to the list"""
        arrangement = self._given_the_list()

        def result():
            return self._when_invalid_item_is_add(arrangement)

        self._then_error_should_be_thrown(result)

    def _given_the_list(self):
        return MetaGameList()

    def _when_invalid_item_is_add(self, arrangement):
        arrangement.add_item('whatever')
        return arrangement

    def _then_error_should_be_thrown(self, result):
        with self.assertRaises(TypeError):
            result()


if __name__ == '__main__':
    unittest.main()
