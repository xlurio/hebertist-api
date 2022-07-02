from scrapy.http import Response
from games_price_digger.src.page_getters.strategies import PageGettingStrategy


class PageGetter():

    def __init__(self, strategy: PageGettingStrategy):
        self._strategy = strategy

    def get_page(self) -> Response:
        return self._strategy.get_page()
