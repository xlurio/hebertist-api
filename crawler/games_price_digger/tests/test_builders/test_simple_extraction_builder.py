import unittest
from unittest.mock import MagicMock
from games_price_digger.src.builders import SimpleExtractionBuilder
from games_price_digger.src.builders.search_page_settings_builder import SearchPageSettingsBuilder
from games_price_digger.src.components.search import Search
from games_price_digger.src.data_diggers.data_digger import DataDigger
from games_price_digger.src.data_getters.strategies.simple_extraction import SimpleExtraction


class SimpleExtractionBuilderTests(unittest.TestCase):
    search = MagicMock(spec=Search)
    data_digger = MagicMock(spec=DataDigger)
    item_title_xpath = 'some_xpath'
    item_link_xpath = '@href'

    def setUp(self) -> None:
        self.builder = SimpleExtractionBuilder()
        self.settings_builder = SearchPageSettingsBuilder()
        self.settings_builder.set_item_title_xpath(self.item_title_xpath)
        self.settings_builder.set_item_link_xpath(self.item_link_xpath)

    def test_building_method(self):
        """Test building SimpleExtraction"""
        self.builder.set_search(self.search)
        self.builder.set_data_digger(self.data_digger)
        self.builder.set_settings_builder(self.settings_builder)
        product = self.builder.build()
        self.assertTrue(isinstance(product, SimpleExtraction))


if __name__ == '__main__':
    unittest.main()
