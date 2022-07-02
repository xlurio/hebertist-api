from scrapy.http import Response
from games_price_digger.src.page_getters.strategies import PageGettingStrategy


class PageGetter():

    def __init__(self, strategy: PageGettingStrategy,
                 url_getter_callback=None,
                 url_getter_parameters: dict = {}):
        self._strategy = strategy
        self._get_url = url_getter_callback
        self._url_getter_parameters = url_getter_parameters

    def set_url_getter_callback(self, url_getter_callback):
        self._get_url = url_getter_callback

    def set_url_getter_parameters(self, url_getter_parameters):
        self._url_getter_parameters = url_getter_parameters

    def get_page(self) -> Response:
        if self._get_url:
            url = self._get_url(**self._url_getter_parameters)
            return self._strategy.get_page(url)
        else:
            raise ValueError('url_getter_callback was not set')
