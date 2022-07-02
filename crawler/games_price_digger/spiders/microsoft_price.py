""" import scrapy

from .utils.helpers import get_price_item
from .utils.price.price_getters.price_getter import RealNumberPriceGetter


class MicrosoftPriceSpider(scrapy.Spider):
    
    name = 'microsoft_price'
    store_name = 'Microsoft Store'
    allowed_domains = ['www.microsoft.com']
    start_urls = ['https://www.microsoft.com/pt-br/store/top-paid/games/pc']
    # Platform search selectors
    game_item_box = ('div[contains(@class, "context-list-page")]/' +
                     'div[@class="m-channel-placement-item"]')
    game_item_title = 'h3'
    game_item_price = 'span[@itemprop="price" and contains(text(), "R$")]'
    next_page_link = 'a[@aria-label = "próxima página"]/@href'
    price_getter = RealNumberPriceGetter(
        real_number_xpath=game_item_price
    )

    # Parameter for the price getter function

    def parse(self, response, **kwargs):
        yield from self.parse_price(response)

    def parse_price(self, response, game=None):
        # Iterate through all the games in Microsoft Store
        search_items = response.xpath('//' + self.game_item_box)
        if search_items:
            yield from self._iterate_games(search_items)
        # Go to the next page
        next_page = response.xpath('//' + self.next_page_link).get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def _iterate_games(self, search_items):
        for item in search_items:
            # For each game in page, get the game title and the game price.
            game = item.xpath('.//' + self.game_item_title + '/text()')
            game = game.get()
            self.price_getter.set_game_box(item)
            price = self.price_getter.get_price()
            yield from self._yield_game_prices(game, price)

    def _yield_game_prices(self, game, price):
        if price:
            yield {
                'price_item': get_price_item(
                    game=game,
                    store=self.store_name,
                    price=price,
                ),
            }
 """
