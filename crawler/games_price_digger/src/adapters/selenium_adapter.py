from selenium.webdriver.remote.webdriver import WebDriver
from games_price_digger.src.builders.web_driver_wait_builder import WebDriverWaitBuilder


class SeleniumAdapter:
    _page_source = ''

    def __init__(self, webdriver):
        self._webdriver = webdriver

    def get_page_source(self, url: str, xpath_of_element_to_find: str) -> str:
        self._webdriver.get(url)
        self._xpath_of_element_to_find = xpath_of_element_to_find
        try:
            self._page_source = self._wait_for_elements()
        finally:
            self._webdriver.close()
            return self._page_source

    def _wait_for_elements(self):
        builder = WebDriverWaitBuilder().set_driver(self._webdriver)
        builder.set_timeout(15)
        builder.set_xpath_of_element_to_wait(self._xpath_of_element_to_find)
        builder.wait()
        self._get_page_source()

    def _get_page_source(self):
        return self._webdriver.page_source
