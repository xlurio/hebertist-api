""" from . import SeleniumPriceSpider, SinglePagePriceParser

from .utils.price.price_getters.price_getter import RealNumberPriceGetter


class GreenManPriceSpider(SeleniumPriceSpider, SinglePagePriceParser):
    
    name = 'greenman_price'
    store_name = 'Greenman Gaming'
    game_box_xpath = 'div[@class="top-section"]'
    game_title_xpath = 'p[@class="prod-name"]'
    game_price_xpath = 'span[@class="current-price"]'

    allowed_domains = ['www.greenmangaming.com']
    start_urls = ['https://www.greenmangaming.com/']
 """
