""" from time import sleep

import scrapy
from selenium.common.exceptions import TimeoutException

from . import SinglePagePriceParser
from .games_metascore import get_game_names
from .utils.helpers import load_chrome_driver, wait_for_element
from .utils.price.price_getters.price_getter import RealNumberPriceGetter


class UbisoftPriceSpider(scrapy.Spider, SinglePagePriceParser):
    
    name = 'ubisoft_price'
    store_name = 'Ubisoft'
    allowed_domains = ['store.ubi.com']
    start_urls = ['https://store.ubi.com/ofertas/home?lang=pt_BR']
    driver = load_chrome_driver()
    # Platform search selectors
    game_box_xpath = 'div[@class="card-details"]'
    game_title_xpath = 'div[@class="prod-title"]'
    game_price_xpath = ('span[@class="sale_price" or ' +
                        'contains(@class, "algolia-product-price")]')
    price_getter = RealNumberPriceGetter(
        real_number_xpath=game_price_xpath
    )
    # Selectors of the elements to wait
    search_field_path = '//input[@class="ais-SearchBox-input"]'
    filter_btn = '//button[contains(@class, "filters-button")]'
    search_results = ('//' + game_box_xpath +
                      '/descendant::' + game_price_xpath)

    def parse(self, response, **kwargs):
        
    # Search and scrape for each game in metacritics
    for game in get_game_names():
        url = self.start_urls[0]
        page_source = self.get_search_results(game)
        request = scrapy.http.Request(
            url=url,
        )
        response = scrapy.http.HtmlResponse(
            url=url,
            request=request,
            body=page_source,
            encoding='utf-8'
        )
        yield from self.parse_price(
            response=response,
            game=game,
        )
        sleep(3)
    self.driver.close()

def get_search_results(self, game):
    
        # Search for the game
        self.driver.get(self.start_urls[0])
        try:
            # Wait for the search bar to load
            search_field = wait_for_element(self.driver,
                                            self.search_field_path)
            search_field.send_keys(game)
            # Wait for the filter button to load
            wait_for_element(self.driver, self.filter_btn)
            # Wait for the prices to load
            wait_for_element(self.driver, self.search_results)
            # Gets the source of the requested URL page
            html = self.driver.page_source
            return html
        except TimeoutException:
            pass
 """
