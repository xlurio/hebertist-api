import time
import urllib.parse
import pandas as pd

from games_price_digger.src.adapters import GameDataFrameAdapter
from games_price_digger.src.builders.found_game_builder import FoundGameBuilder
from games_price_digger.src.builders.simple_extraction_builder import SimpleExtractionBuilder
from games_price_digger.src.builders.search_builder import SearchBuilder
from games_price_digger.src.data_diggers.data_digger import DataDigger
from games_price_digger.src.data_diggers.strategies.price_digging_strategies.real_number_digging import RealNumberDigging
from games_price_digger.src.data_diggers.strategies.search_page_digging import SearchPageDigging
from games_price_digger.src.data_getters.page_data_extractor import PageDataExtractor
from games_price_digger.src.data_getters.strategies import simple_extraction
from games_price_digger.src.data_getters.strategies.simple_extraction import SimpleExtraction
from games_price_digger.src.game_name_getter import GameNamesGetter
from games_price_digger.src.lists import GameBoxList
from games_price_digger.src.page_getters.page_getter import PageGetter
from games_price_digger.src.page_getters.strategies import SimplePage

from scrapy import Spider

try:
    from core.models import GameModel
except ModuleNotFoundError:
    pass


class GenericSpider(Spider):
    name = 'simple_spider'

    store_name = None
    game_box_xpath = None
    game_title_xpath = None
    game_price_xpath = None
    game_link_xpath = None

    try:
        _games_in_database = GameModel.objects.all().values()

    except NameError:
        _games_in_database = pd.DataFrame({
            'name': ['error'],
            'price': ['0.00'],
        })

    _game_dataframe = pd.DataFrame(_games_in_database)
    _game_data = GameDataFrameAdapter(_game_dataframe, 'name')
    _name_getter = GameNamesGetter()

    page_getting_strategy = SimplePage()
    digging_strategy = SearchPageDigging()
    _data_extractor = PageDataExtractor()

    _search_builder = SearchBuilder()
    extraction_strategy_builder = SimpleExtractionBuilder()

    allowed_domains = ['']
    start_urls = ['']

    def __init__(self):
        self.game_box_xpath = f'//{self.game_box_xpath}'

        self._page_getter = PageGetter(self.page_getting_strategy)
        self._page_getter.set_url_getter_callback(self._get_search_url)

        _price_digging_strategy = self.get_price_digging_strategy()

        self.digging_strategy.set_strategy(_price_digging_strategy)
        self._data_digger = DataDigger(self.digging_strategy)

        self.extraction_strategy_builder.set_item_title_xpath(
            self.game_title_xpath
        )
        self.extraction_strategy_builder.set_item_link_xpath(
            self.game_link_xpath
        )
        self.extraction_strategy_builder.set_data_digger(
            self._data_digger
        )

        self._search_builder.set_store(self.store_name)

    def get_price_digging_strategy(self):
        """Override this method to change the price digging strategy"""
        return RealNumberDigging(self.game_price_xpath)

    def _get_search_url(self, game):
        pass

    def parse(self, response, **kwargs):
        for game in self._name_getter.yield_names(self._game_data):

            self._search_builder.set_game(game)
            self.search = self._search_builder.build()

            self.extraction_strategy_builder.set_search(self.search)
            simple_extraction = self.extraction_strategy_builder.build()

            self._data_extractor.set_strategy(simple_extraction)

            url_getter_parameters = {'game': game}
            self._page_getter.set_url_getter_parameters(
                url_getter_parameters
            )
            response = self._page_getter.get_page()

            yield from self._parse_price(response)

            time.sleep(3)

    def _parse_price(self, response):
        game_boxes = response.xpath(self.game_box_xpath)
        game_box_list = GameBoxList(*game_boxes)
        game_data = self._data_extractor.extract_data(game_box_list)
        iterator = game_data.make_iterator()

        there_is_items_in_list = not iterator.is_done()

        while there_is_items_in_list:
            current_index = iterator.get_index()
            current_item = game_data.get_item_at(current_index)
            yield from self._validate_data(current_item, self.search)

            iterator.next()
            there_is_items_in_list = not iterator.is_done()

    def _validate_data(self, game, search):
        game_name = game.get_name()
        has_name = len(game_name) > 0

        game_price = game.get_price()
        has_price = game_price > 0.00

        game_link = game.get_link()
        has_link = len(game_link) > 0

        if has_name and has_price and has_link:
            yield {
                'game': game,
                'search': search,
            }
