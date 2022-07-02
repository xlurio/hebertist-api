""" import scrapy

from .utils.helpers import get_price_item
from .utils.price.price_getters.price_getter import RealNumberPriceGetter


class RockstarPriceSpider(scrapy.Spider):
    
    name = 'rockstar_price'
    allowed_domains = ['store.rockstargames.com']
    start_urls = ['http://store.rockstargames.com/']
    # Platform search selectors
    platform_games = ('a[contains(@href, "/game/") and @class="css-y7dule"]/' +
                      '@href')
    game_item_box = 'ul[@class="css-ff7aca"]/li'
    game_item_title = 'h3'
    game_item_price = 'div[@class="css-l0l07p"]'
    price_getter = RealNumberPriceGetter(
        real_number_xpath=game_item_price
    )

    def parse(self, response, **kwargs):
        game_links = response.xpath('//' + self.platform_games).getall()
        if game_links:
            yield from self._crawl_game_pages(game_links)

    def _crawl_game_pages(self, response, game_links):
        for link in game_links:
            game_page = response.urljoin(link)
            yield scrapy.Request(url=game_page, callback=self.parse_price)

    def parse_price(self, response, game=None):
        game_editions = response.xpath('//' + self.game_item_box)
        if game_editions:
            yield from self._iterate_game_editions(game_editions)

    def _iterate_game_editions(self, game_editions):
        for edition in game_editions:
            game = edition.xpath('.//' + self.game_item_title + '/text()')
            game = game.get()
            self.price_getter.set_game_box(edition)
            price = self.price_getter.get_price()

            yield {
                'price_item': get_price_item(
                    game=game,
                    store='Rockstar Store',
                    price=price,
                ),
            }
 """
