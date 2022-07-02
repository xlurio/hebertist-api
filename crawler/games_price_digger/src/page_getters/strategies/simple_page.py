import requests

from scrapy import Selector
from . import PageGettingStrategy


class SimplePage(PageGettingStrategy):

    def __init__(self, url_getter_callback,
                 page_getting_parameters: dict = {}) -> None:
        get_url = url_getter_callback
        self._url = get_url(**page_getting_parameters)

    def get_page(self):
        url_request = requests.get(self._url)
        response = Selector(
            text=url_request.text
        )
        return response
