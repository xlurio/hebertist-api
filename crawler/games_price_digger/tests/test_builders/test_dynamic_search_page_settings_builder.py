import unittest
from games_price_digger.src.builders import DynamicSearchPageSettingsBuilder
from games_price_digger.src.data_structures.dynamic_search_page_settings \
    import DynamicSearchPageSettings


class DynamicSearchPageSettingsBuilderTests(unittest.TestCase):

    def test_build(self):
        """Test building product"""
        result = self._when_product_is_built()
        self._then_product_must_have_right_interface(result)

    def _when_product_is_built(self):
        builder = DynamicSearchPageSettingsBuilder()
        builder.set_url('https://builder.test.com/')
        builder.set_game_to_search('Awesome Game')
        builder.set_xpath_to_element_to_wait('div[@id="element_to_wait"]')
        builder.set_xpath_to_search_bar('input[@id="search-bar"]')
        return builder.build()

    def _then_product_must_have_right_interface(self, product):
        self.assertTrue(isinstance(product, DynamicSearchPageSettings))


if __name__ == '__main__':
    unittest.main()
