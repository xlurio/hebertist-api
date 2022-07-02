""" import urllib.parse

from . import SinglePagePriceParser, ScrapyPriceSpider
from .utils.price.price_getters.price_getter import (
    SeparatedIntegerAndDecimalsPriceGetter
)


class NuuvemPriceParser(ScrapyPriceSpider, SinglePagePriceParser):
    name = 'nuuvem_price'
    store_name = 'Nuuvem'
    game_box_xpath = 'a[@class="product-card--wrapper"]'
    game_title_xpath = 'h3'
    game_price_integer_xpath = 'span[@class="integer"]'
    game_price_decimal_xpath = 'span[@class="decimal"]'
    price_getter = SeparatedIntegerAndDecimalsPriceGetter(
        integer_xpath=game_price_integer_xpath,
        decimals_xpath=game_price_decimal_xpath,
    )

    allowed_domains = ['www.nuuvem.com']
    start_urls = ['https://www.nuuvem.com/']

    def _get_search_url(self, game):
        encoded_name = urllib.parse.quote(game)
        return (f'{self.start_urls[0]}catalog/platforms/pc/'
                f'search/{encoded_name}')
 """
