class DynamicSearchPageSettings:

    def __init__(self, url: str, xpath_to_search_bar: str, game_to_search: str,
                 xpath_to_element_to_wait: str):
        self._url = url
        self._xpath_to_search_bar = f'//{xpath_to_search_bar}'
        self._game_to_search = game_to_search
        self._xpath_to_element_to_wait = f'//{xpath_to_element_to_wait}'

    def get_url(self):
        return self._url

    def get_xpath_to_search_bar(self):
        return self._xpath_to_search_bar

    def get_game_to_search(self):
        return self._game_to_search

    def get_xpath_to_element_to_wait(self):
        return self._xpath_to_element_to_wait
