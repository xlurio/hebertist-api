import unittest
from games_price_digger.src.data_structures import DynamicSearchPageSettings


class DynamicSearchPageSettingsTests(unittest.TestCase):
    _fake_url = 'https://game.store.com/awesome-game/'
    _fake_search_bar = 'input[@id="search-bar"]'
    _fake_game = 'Awesome Game'
    _fake_element = 'div[@id="element-to-wait"]'

    def test_url_getter(self):
        """Test url getter"""
        result = self._when_the_search_page_is_setted()
        self._then_is_must_return_url_in(result)

    def _then_is_must_return_url_in(self, settings: DynamicSearchPageSettings):
        url = settings.get_url()
        expected_url = self._fake_url
        self.assertEqual(url, expected_url)

    def test_xpath_to_search_bar_getter(self):
        """Test xpath_to_search_bar getter"""
        result = self._when_the_search_page_is_setted()
        self._then_is_must_return_xpath_to_search_bar_in(result)

    def _then_is_must_return_xpath_to_search_bar_in(
        self, settings: DynamicSearchPageSettings
    ):
        xpath_to_search_bar = settings.get_xpath_to_search_bar()
        expected_xpath_to_search_bar = f'//{self._fake_search_bar}'
        self.assertEqual(xpath_to_search_bar, expected_xpath_to_search_bar)

    def test_game_to_search_getter(self):
        """Test game_to_search getter"""
        result = self._when_the_search_page_is_setted()
        self._then_is_must_return_game_to_search_in(result)

    def _then_is_must_return_game_to_search_in(
        self, settings: DynamicSearchPageSettings
    ):
        game_to_search = settings.get_game_to_search()
        expected_game_to_search = self._fake_game
        self.assertEqual(game_to_search, expected_game_to_search)

    def test_xpath_to_element_to_wait_getter(self):
        """Test xpath_to_element_to_wait getter"""
        result = self._when_the_search_page_is_setted()
        self._then_is_must_return_xpath_to_element_to_wait_in(result)

    def _then_is_must_return_xpath_to_element_to_wait_in(
        self, settings: DynamicSearchPageSettings
    ):
        xpath_to_element_to_wait = settings.get_xpath_to_element_to_wait()
        expected_xpath_to_element_to_wait = f'//{self._fake_element}'
        self.assertEqual(
            xpath_to_element_to_wait, expected_xpath_to_element_to_wait
        )

    def _when_the_search_page_is_setted(self):
        return self._make_search_page_settings()

    def _make_search_page_settings(self):
        settings = DynamicSearchPageSettings(
            url=self._fake_url,
            xpath_to_search_bar=self._fake_search_bar,
            game_to_search=self._fake_game,
            xpath_to_element_to_wait=self._fake_element
        )
        return settings


if __name__ == '__main__':
    unittest.main()
