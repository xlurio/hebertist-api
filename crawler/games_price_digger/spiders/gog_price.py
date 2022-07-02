import urllib.parse

from games_price_digger.spiders.interfaces.generic_spider import GenericSpider


class GogPriceSpider(GenericSpider):
    _testing_html_file = 'gog_test.html'

    name = 'gog_price'
    store_name = 'GOG.com'

    game_box_xpath = 'a[starts-with(@class, "product-tile")]'
    game_title_xpath = 'p[@class="product-tile__title"]'
    game_price_xpath = 'span[@class="product-tile__price--final"]'
    game_link_xpath = '@href'

    allowed_domains = ['www.gog.com']
    start_urls = ['https://www.gog.com/en/']

    def get_search_url(self, game):
        encoded_name = urllib.parse.quote(game)
        return (f'{self.start_urls[0]}games?query={encoded_name}' +
                '&order=asc:title')
