import unittest
from unittest.mock import MagicMock

from scrapy import Selector
from games_price_digger.src.builders import SearchPageSettingsBuilder
from games_price_digger.src.data_structures.digging_settings\
    .search_page_settings import SearchPageSettings

mocked_selector = MagicMock(spec=Selector)


class SearchPageSettingsBuilderTests(unittest.TestCase):

    def test_build(self):
        """Test building product"""
        result = self._when_product_is_built()
        self._then_product_must_have_right_interface(result)

    def _when_product_is_built(self):
        builder = SearchPageSettingsBuilder()
        builder.set_item_box(mocked_selector)
        builder.set_item_title_xpath('h2')
        builder.set_item_link_xpath('@href')
        return builder.build()

    def _then_product_must_have_right_interface(self, product):
        self.assertTrue(isinstance(product, SearchPageSettings))


if __name__ == '__main__':
    unittest.main()
