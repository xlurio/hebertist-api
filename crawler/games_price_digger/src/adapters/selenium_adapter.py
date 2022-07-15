from selenium.webdriver.remote.webdriver import WebDriver
from games_price_digger.src.builders.web_driver_wait_builder import \
    WebDriverWaitBuilder
from games_price_digger.src.data_structures.dynamic_search_page_settings \
    import DynamicSearchPageSettings


class SeleniumAdapter:
    _page_source = ''

    def __init__(self, webdriver: WebDriver):
        self._webdriver = webdriver

    def get_search_page_source(
        self, settings: DynamicSearchPageSettings
    ) -> str:
        url = settings.get_url()
        self._webdriver.get(url)

        self._settings = settings

        try:
            self._page_source = self._wait_for_elements()
        finally:
            self._webdriver.close()
            return self._page_source

    def _wait_for_elements(self):
        xpath_to_search_bar = self._settings.get_xpath_to_search_bar()
        game_to_search = self._settings.get_game_to_search()
        xpath_of_element_to_wait = self._settings.get_xpath_to_search_bar()

        builder = WebDriverWaitBuilder().set_driver(self._webdriver)
        builder.set_timeout(15)
        builder.set_xpath_of_element_to_wait(xpath_to_search_bar)
        search_bar = builder.wait()

        search_bar.send_keys(game_to_search)
        builder.set_xpath_of_element_to_wait(xpath_of_element_to_wait)

        return self._get_page_source()

    def _get_page_source(self):
        return self._webdriver.page_source
