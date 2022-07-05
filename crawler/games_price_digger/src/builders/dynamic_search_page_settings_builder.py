from games_price_digger.src.data_structures.dynamic_search_page_settings import DynamicSearchPageSettings


class DynamicSearchPageSettingsBuilder:

    def set_url(self, url: str):
        self._url = url
        return self

    def set_xpath_to_search_bar(self, xpath_to_search_bar: str):
        self._xpath_to_search_bar = xpath_to_search_bar
        return self

    def set_game_to_search(self, game_to_search: str):
        self._game_to_search = game_to_search
        return self

    def set_xpath_to_element_to_wait(self, xpath_to_element_to_wait: str):
        self._xpath_to_element_to_wait = xpath_to_element_to_wait
        return self

    def build(self):
        return DynamicSearchPageSettings(
            self._url,
            self._xpath_to_search_bar,
            self._game_to_search,
            self._xpath_to_element_to_wait,
        )
