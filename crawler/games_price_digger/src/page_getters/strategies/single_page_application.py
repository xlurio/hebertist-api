from scrapy import Selector
from games_price_digger.src.adapters.selenium_adapter import SeleniumAdapter
from games_price_digger.src.data_structures.dynamic_search_page_settings import DynamicSearchPageSettings
from . import PageGettingStrategy


class SinglePageApplication(PageGettingStrategy):

    def __init__(self, webdriver_adapter: SeleniumAdapter,
                 search_page_settings: DynamicSearchPageSettings) -> None:
        self._webdriver_adapter = webdriver_adapter
        self._search_page_settings = search_page_settings

    def get_page(self):
        page_source = self._webdriver_adapter.get_search_page_source(
            self._search_page_settings
        )
        response = Selector(text=page_source)
        return response
