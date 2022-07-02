import logging
import unittest
from unittest.mock import MagicMock
from games_price_digger.src.components import Search
from games_price_digger.src.components.found_game import FoundGame
from games_price_digger.src.data_diggers.strategies.search_page_digging import SearchPageDigging
from games_price_digger.src.data_getters.strategies import SimpleExtraction
from games_price_digger.src.lists.game_box_list import GameBoxList
from games_price_digger.src.utils.fake_response_builders.html_response_builder import HTMLResponseBuilder
from games_price_digger.src.utils.test_html_getter import TestHTMLGetter

search_page_digging = MagicMock(spec=SearchPageDigging)
search_page_digging.dig_data.return_value = {
    'name': 'Generic Title',
    'price': 2.99,
    'link': 'https://store.steam.com/generic-title/'
}


class SimpleExtractionTests(unittest.TestCase):
    fake_response_builder = HTMLResponseBuilder()
    test_html_getter = TestHTMLGetter()
    search = Search(
        game='Generic Title',
        store='Steam',
    )
    item_box_xpath = '//section'
    game_name = 'Generic Title'
    game_price = 2.99
    game_link = 'https://store.steam.com/generic-title/'

    def setUp(self):
        html_file_path = self.test_html_getter.get_html_file_by_name(
            'generic.html'
        )
        self.fake_response_builder.set_html_file_path(html_file_path)
        response = self.fake_response_builder.build()

        game_boxes = response.xpath(self.item_box_xpath)
        self.game_box_list = GameBoxList(*game_boxes)

        self.simple_extraction = SimpleExtraction(
            item_title_xpath='h2',
            item_link_xpath='@href',
            search=self.search,
            data_digger=search_page_digging
        )

    def test_extract_data(self):
        """Test extract_data() method"""
        expected_result = self._get_fake_game_list()
        result_list = self.simple_extraction.extract_data(self.game_box_list)
        iterator = result_list.make_iterator()
        result = []
        while not iterator.is_done():
            current_index = iterator.get_index()
            current_item = result_list.get_item_at(current_index)
            result.append(current_item)
            iterator.next()
        self.assertEqual(result, expected_result)

    def _get_fake_game_list(self):
        game = FoundGame(
            name=self.game_name,
            price=self.game_price,
            link=self.game_link
        )
        return [game]


if __name__ == '__main__':
    unittest.main()
