import unittest
from games_price_digger.src.builders import FoundGameBuilder
from games_price_digger.src.components.found_game import FoundGame


class FoundGameBuilderTests(unittest.TestCase):

    def test_build(self):
        """Test building product"""
        result = self._when_product_is_built()
        self._then_product_must_have_right_interface(result)

    def _when_product_is_built(self):
        builder = FoundGameBuilder()
        builder.set_name('Awesome Game')
        builder.set_link('https://game.store.com/awesome-game/')
        builder.set_price(20.99)
        return builder.build()

    def _then_product_must_have_right_interface(self, product):
        self.assertTrue(isinstance(product, FoundGame))


if __name__ == '__main__':
    unittest.main()
