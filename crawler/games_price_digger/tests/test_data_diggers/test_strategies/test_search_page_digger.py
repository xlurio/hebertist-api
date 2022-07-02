import unittest
from games_price_digger.src.components import FoundGame
from games_price_digger.src.data_diggers.strategies import SearchPageDigging
from unittest.mock import MagicMock
from games_price_digger.src.data_diggers.strategies.price_digging_strategies.price_digging_strategy import PriceDiggingStrategy

from games_price_digger.src.utils.fake_response_builders import HTMLResponseBuilder
from games_price_digger.src.utils import TestHTMLGetter


class SearchPageDiggingTests(unittest.TestCase):
    price_digging_strategy = MagicMock(spec=PriceDiggingStrategy)
    fake_response_builder = HTMLResponseBuilder()
    test_html_getter = TestHTMLGetter()
    fake_price = 2.99
    item_title_xpath = 'h2'
    item_link_xpath = '@href'

    def setUp(self):
        self.price_digging_strategy.dig_data.return_value = self.fake_price
        self.search_page_digging = SearchPageDigging(
            self.price_digging_strategy
        )

        html_file_path = self.test_html_getter.get_html_file_by_name(
            'generic.html'
        )
        self.fake_response_builder.set_html_file_path(html_file_path)
        response = self.fake_response_builder.build()

        item_box_xpath = '//section'
        self.item_box = response.xpath(item_box_xpath)

    def test_dig_data(self):
        """Test dig_data() method"""
        expected_result = {
            'name': 'Generic Title',
            'price': self.fake_price,
            'link': 'https://store.steam.com/generic-title/',
        }
        result = self.search_page_digging.dig_data(
            item_box=self.item_box,
            item_title_xpath=self.item_title_xpath,
            item_link_xpath=self.item_link_xpath,
        )
        self.assertEqual(result['name'], expected_result['name'])
        self.assertAlmostEqual(result['price'], expected_result['price'])
        self.assertEqual(result['link'], expected_result['link'])


if __name__ == '__main__':
    unittest.main()
