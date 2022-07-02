import unittest
from unittest.mock import MagicMock
from games_price_digger.spiders.steam_price import SteamPriceSpider
from games_price_digger.src.game_name_getter.game_names_getter import GameNamesGetter
from games_price_digger.src.page_getters.page_getter import PageGetter
from games_price_digger.src.utils.fake_response_builders.html_response_builder import HTMLResponseBuilder
from games_price_digger.src.utils.test_html_getter import TestHTMLGetter

mocked_name_getter = MagicMock(spec=GameNamesGetter)

mocked_page_getter = MagicMock(spec=PageGetter)


class SteamPriceTests(unittest.TestCase):
    test_game_name = 'My Time At Portia'
    store = 'Steam'

    def setUp(self) -> None:
        html_getter = TestHTMLGetter()
        html_path = html_getter.get_html_file_by_name('steam_test.html')

        fake_response_builder = HTMLResponseBuilder()
        fake_response_builder.set_html_file_path(html_path)
        self.fake_response = fake_response_builder.build()

        mocked_name_getter.yield_names.return_value = iter(
            [self.test_game_name]
        )
        mocked_page_getter.get_page.return_value = self.fake_response

        self.spider = SteamPriceSpider()
        self.spider._name_getter = mocked_name_getter
        self.spider._page_getter = mocked_page_getter

    def test_parse(self):
        """Test parse() method"""
        parsed_data = self.when_data_is_parsed()
        self.then_it_should_yield_game_data(parsed_data)

    def when_data_is_parsed(self):
        parsed_data = [data for data in self.spider.parse(self.fake_response)]
        return parsed_data

    def then_it_should_yield_game_data(self, parsed_data):
        first_item = parsed_data[0]

        parsed_game = first_item.get('game')
        game_price = parsed_game.get_price()
        game_link = parsed_game.get_link()

        parsed_search = first_item.get('search')
        search_game = parsed_search.get_game()
        search_store = parsed_search.get_store()

        expected_price = 79.90

        expected_protocol = 'https://'
        expected_domain = 'store.steampowered.com'
        expected_route = '/app/666140/My_Time_At_Portia/'
        expected_parameters = '?snr=1_7_7_151_150_1'
        expected_url = (
            f'{expected_protocol}{expected_domain}{expected_route}'
            f'{expected_parameters}'
        )

        self.assertEqual(search_game, self.test_game_name)
        self.assertEqual(search_store, self.store)
        self.assertAlmostEqual(game_price, expected_price)
        self.assertEqual(game_link, expected_url)


if __name__ == '__main__':
    unittest.main()
