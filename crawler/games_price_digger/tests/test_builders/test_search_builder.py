import unittest
from games_price_digger.src.builders import SearchBuilder
from games_price_digger.src.components.search import Search


class SearchBuilderTests(unittest.TestCase):

    def test_build(self):
        """Test building product"""
        result = self._when_product_is_built()
        self._then_product_must_have_right_interface(result)

    def _when_product_is_built(self):
        builder = SearchBuilder()
        builder.set_game('Awesome Game')
        builder.set_store('Store')
        return builder.build()

    def _then_product_must_have_right_interface(self, product):
        self.assertTrue(isinstance(product, Search))


if __name__ == '__main__':
    unittest.main()
