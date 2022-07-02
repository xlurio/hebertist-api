import requests

from scrapy import Selector
from . import PageGettingStrategy


class SimplePage(PageGettingStrategy):

    def get_page(self, url: str):
        url_request = requests.get(url)
        response = Selector(
            text=url_request.text
        )
        return response
