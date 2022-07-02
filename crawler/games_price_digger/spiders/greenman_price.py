from games_price_digger.src.adapters.selenium_adapter import SeleniumAdapter
from games_price_digger.src.factories.chrome_driver_factory import ChromeDriveFactory
from games_price_digger.src.page_getters.strategies.single_page_application import SinglePageApplication
from . import GenericSpider


class GreenManPriceSpider(GenericSpider):
    _testing_html_file = 'greenman_test.html'

    name = 'greenman_price'
    store_name = 'Greenman Gaming'
    game_box_xpath = 'div[@class="top-section"]'
    game_title_xpath = 'p[@class="prod-name"]'
    game_price_xpath = 'span[@class="current-price"]'

    allowed_domains = ['www.greenmangaming.com']
    start_urls = ['https://www.greenmangaming.com/']

    webdriver_factory = ChromeDriveFactory()

    def get_page_getting_strategy(self, **kwargs):
        webdriver = self.webdriver_factory.make_driver()
        webdriver_adapter = SeleniumAdapter(webdriver)
        url = self.start_urls[0]
        element_to_find_xpath = self.game_box_xpath
        return SinglePageApplication(
            webdriver_adapter, url, element_to_find_xpath
        )
