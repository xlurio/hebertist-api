import urllib

from games_price_digger.spiders.interfaces.generic_spider import GenericSpider


class SteamPriceSpider(GenericSpider):
    _testing_html_file = 'steam_test.html'

    name = 'steam_price'
    store_name = 'Steam'

    game_box_xpath = 'a[starts-with(@class, "search_result_row ")]'
    game_title_xpath = 'span[@class="title"]'
    game_price_xpath = (
        'div[contains(@class, " search_price ")]'
    )
    game_link_xpath = '@href'

    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/']

    def get_search_url(self, game):
        encoded_name = urllib.parse.quote(game)
        return (f'{self.start_urls[0]}search/?term={encoded_name}' +
                '&category1=998')
