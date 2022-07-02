""" import urllib.parse
from time import sleep

import scrapy
from scrapy.selector import Selector
from selenium.common.exceptions import TimeoutException

from . import Search
from .games_metascore import get_game_names
from .utils.helpers import get_page_source, load_chrome_driver
from .utils.helpers import get_price_item
from .utils.helpers import wait_for_element
from .utils.price.price_getters.price_getter import RealNumberPriceGetter


class OriginPriceSpider(scrapy.Spider):
    
    name = 'origin_price'
    store_name = 'Origin'
    allowed_domains = ['www.origin.com']
    start_urls = ['https://www.origin.com/']
    # Platform search selectors
    game_item_box = 'a[contains(@class, "home-tile")]'
    game_item_title = 'h1'
    game_item_link = game_item_box + '/@href'
    # Game page selectors
    game_item_price = 'button/span'
    buy_btn_path = ('//div[@class="origin-store-gdp-header-block" ' +
                    'and position()=1]/descendant::button[1]')
    game_item_price_box_one = ('th[contains(@class,' +
                               '"origin-store-pdp-comparison-table-cta")]')
    game_item_price_box_two = \
        'origin-store-osp-interstitial-premier-purchase-cta'

    # Parameter for the price getter function

    def get_parsing_args_list(self):
        # Method returns list of possible XPATHs to the game price
        parsing_args_one = {
            'game_item_price_box': self.game_item_price_box_one,
        }
        parsing_args_two = {
            'game_item_price_box': self.game_item_price_box_two,
        }
        return [parsing_args_one, parsing_args_two]

    def _get_search_url(self, game):
        encoded_name = urllib.parse.quote(game)
        return (f'{self.start_urls[0]}bra/pt-br/store/browse?' +
                f'searchString={encoded_name}&fq=gameType:basegame,' +
                'platform:pc-download')

    def parse(self, response, **kwargs):
        
    # Search and scrape for each game in metacritics
    for game in get_game_names():
        search = Search(
            game=game,
            store=self.store_name,
        )
        # Get search URL and page loaded with JavaScript
        url = self._get_search_url(game)

        to_wait_element = '//' + self.game_item_box
        res = Selector(text=get_page_source(url, to_wait_element))

        # Get search results
        search_items = res.xpath('//' + self.game_item_box)

        # Iterate through gotten information
        yield from self._iterate_games_found(res, search, search_items)
        sleep(3)

def _iterate_games_found(self, res, search, search_items):
    for item in search_items:
        yield from self._check_if_some_game_was_found(res, search, item)

def _check_if_some_game_was_found(self, res, search, item):
    search_game = \
        item.xpath(f'.//descendant::{self.game_item_title}/' +
                   'text()')
    if search_game:
        yield from self._check_if_is_the_right_game(
            search_game, res, search
        )

def _check_if_is_the_right_game(self, search_game, res, search):
    search_game = str(search_game.get()).strip()
    if search.is_the_searched_game(search_game):
        game_link = 'https://' + self.allowed_domains[0]
        game_link += res.xpath(
            '//' + self.game_item_link
        ).get()
        yield from self.parse_game_page(game=search.game,
                                        url=game_link)

def parse_game_page(self, game, url):
    # Get buying page
    driver = load_chrome_driver()
    driver.get(url)
    try:
        yield from self._choose_price_xpath(driver, game)
    finally:
        driver.close()

def _choose_price_xpath(self, driver, game):
    price_box = {}
    buy_btn = wait_for_element(driver, self.buy_btn_path)
    buy_btn.click()
    for args in self.get_parsing_args_list():
        price_box = self._check_if_price_xpath_works(driver, args)
    html = driver.page_source
    yield from self.parse_price(game=game, html=html, **price_box)

def _check_if_price_xpath_works(self, driver, args):
    to_wait_element = ('//' + args['game_item_price_box'] +
                       '/descendant::' + self.game_item_price)
    try:
        wait_for_element(driver, to_wait_element)
        return args
    except TimeoutException:
        pass

def parse_price(self, game, html, game_item_price_box):
    # Get source code of game page
    res = Selector(text=html)
    # Get price of each edition
    price_boxes = res.xpath('//' + game_item_price_box)
    if price_boxes:
        yield from self._iterate_game_editions(game, price_boxes)

def _iterate_game_editions(self, game, price_boxes):
    for item in price_boxes:
        price_getter = RealNumberPriceGetter(
            real_number_xpath=self.game_item_price
        )
        price_getter.set_game_box(item)
        price = price_getter.get_price()
        yield {
            'price_item': get_price_item(
                game=game,
                store='Origin',
                price=price,
            ),
        }
"""
