from games_price_digger.src.adapters.selenium_adapter import SeleniumAdapter
from . import PageGettingStrategy


class SinglePageApplication(PageGettingStrategy):

    def __init__(self, webdriver_adapter: SeleniumAdapter, url: str,
                 element_to_find_xpath: str) -> None:
        self._webdriver_adapter = webdriver_adapter
        self._url = url
        self._element_to_find_xpath = element_to_find_xpath

    def get_page(self):
        return self._webdriver_adapter.get_page_source(
            self._url, self._element_to_find_xpath
        )
