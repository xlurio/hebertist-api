from games_price_digger.src.adapters.selenium_adapter import SeleniumAdapter
from games_price_digger.src.builders.dynamic_search_page_settings_builder \
    import DynamicSearchPageSettingsBuilder
from games_price_digger.src.factories.chrome_driver_factory import \
    ChromeDriveFactory
from games_price_digger.src.page_getters.strategies.single_page_application \
    import SinglePageApplication
from . import GenericSpider


class GreenManPriceSpider(GenericSpider):
    _testing_html_file = 'greenman_test.html'

    name = 'greenman_price'
    store_name = 'Greenman Gaming'
    game_box_xpath = 'ol/li'
    game_title_xpath = 'p[@class="prod-name"]'
    game_price_xpath = 'span[@class="current-price"]'
    game_link_xpath = 'descendant::a[string-length(@title) < 1]/@href'
    search_bar_xpath = 'input[@id="search-input"]'

    allowed_domains = ['www.greenmangaming.com']
    start_urls = ['https://www.greenmangaming.com/']

    webdriver_factory = ChromeDriveFactory()

    def get_page_getting_strategy(self, **kwargs):
        settings_builder = DynamicSearchPageSettingsBuilder()
        url = self.start_urls[0]
        settings_builder.set_url(url)
        settings_builder.set_xpath_to_search_bar(self.search_bar_xpath)
        game_to_search = kwargs.get('game')
        settings_builder.set_game_to_search(game_to_search)
        xpath_to_element_to_wait = self.game_box_xpath
        settings_builder.set_xpath_to_element_to_wait(xpath_to_element_to_wait)

        webdriver = self.webdriver_factory.make_driver()
        webdriver_adapter = SeleniumAdapter(webdriver)

        search_page_settings = settings_builder.build()

        return SinglePageApplication(
            webdriver_adapter, search_page_settings
        )

    def validate_link(self, link):
        store_url = self.start_urls[0]

        if link[0] == '/':
            link = link[1:]

        return f'{store_url}{link}'
