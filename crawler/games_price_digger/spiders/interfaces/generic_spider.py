import time
import pandas as pd
import django

from games_price_digger.src.adapters import GameDataFrameAdapter
from games_price_digger.src.builders.simple_extraction_builder import SimpleExtractionBuilder
from games_price_digger.src.builders.search_builder import SearchBuilder
from games_price_digger.src.components.game import Game
from games_price_digger.src.components.search import Search
from games_price_digger.src.data_diggers.data_digger import DataDigger
from games_price_digger.src.data_diggers.strategies.price_digging_strategies.real_number_digging import RealNumberDigging
from games_price_digger.src.data_diggers.strategies.search_page_digging import SearchPageDigging
from games_price_digger.src.data_getters.page_data_extractor import PageDataExtractor
from games_price_digger.src.game_name_getters import GameNamesGetter
from games_price_digger.src.lists import GameBoxList
from games_price_digger.src.lists.search_game_list import SearchGameList
from games_price_digger.src.page_getters.page_getter import PageGetter
from games_price_digger.src.page_getters.strategies import SimplePage
from django.core.exceptions import AppRegistryNotReady
from scrapy import Spider
from games_price_digger.src.utils.fake_response_builders.html_response_builder import HTMLResponseBuilder

from games_price_digger.src.utils.test_html_getter import TestHTMLGetter

try:
    from core.models import GameModel
except AppRegistryNotReady:
    django.setup()
    from core.models import GameModel


class GenericSpider(Spider):
    _games_in_database = GameModel.objects.all().values()

    _testing_html_file = None

    _data_extractor_class = PageDataExtractor
    _game_dataframe = pd.DataFrame(_games_in_database)
    _game_data = GameDataFrameAdapter(_game_dataframe, 'name')
    _name_getter = GameNamesGetter()
    _search_builder = SearchBuilder()

    name = 'generic_spider'

    store_name = None
    game_box_xpath = None
    game_title_xpath = None
    game_price_xpath = None
    game_link_xpath = None

    digging_strategy_class = SearchPageDigging
    extraction_strategy_builder = SimpleExtractionBuilder()

    allowed_domains = ['']
    start_urls = ['']

    def __init__(self):
        self.game_box_xpath = f'//{self.game_box_xpath}'
        self._make_data_digger()

    def _make_data_digger(self):
        _price_digging_strategy = self.get_price_digging_strategy()
        self._digging_strategy = self.digging_strategy_class(
            _price_digging_strategy
        )
        self._data_digger = DataDigger(self._digging_strategy)

    def get_price_digging_strategy(self):
        """Override this method to set the price digging strategy"""
        return RealNumberDigging(self.game_price_xpath)

    def parse(self, response, **kwargs):
        for game in self._name_getter.yield_names(self._game_data):
            self._make_search(game)
            self._make_data_extractor()

            response = self._check_for_test_environment(game, **kwargs)

            yield from self._parse_price(response)

            time.sleep(3)

    def _make_search(self, game: str):
        self._search_builder.set_store(self.store_name)
        self._search_builder.set_game(game)
        self.search = self._search_builder.build()

    def _make_data_extractor(self):
        digging_settings_builder = self._digging_strategy.make_settings_builder(
            self.game_title_xpath,
            self.game_link_xpath,
        )

        search_games_list = self.make_games_list()

        self.extraction_strategy_builder.set_settings_builder(
            digging_settings_builder
        )
        self.extraction_strategy_builder.set_data_digger(
            self._data_digger
        )
        self.extraction_strategy_builder.set_search_items_list(
            search_games_list
        )
        extraction_strategy = self.extraction_strategy_builder.build()

        self.data_extractor = self._data_extractor_class(extraction_strategy)

    def make_games_list(self):
        """Override this method to set the games list for the extraction 
        strategy"""
        return SearchGameList(self.search)

    def _check_for_test_environment(self, game, **kwargs):
        if kwargs.get('testing'):
            return self._make_fake_response()
        return self._get_page_response(game)

    def _make_fake_response(self):
        html_getter = TestHTMLGetter()
        html_path = html_getter.get_html_file_by_name(
            self._testing_html_file
        )

        fake_response_builder = HTMLResponseBuilder()
        fake_response_builder.set_html_file_path(html_path)
        return fake_response_builder.build()

    def _get_page_response(self, game):
        page_getting_parameters = {'game': game}
        _page_getting_strategy = self.get_page_getting_strategy(
            **page_getting_parameters
        )
        _page_getter = PageGetter(_page_getting_strategy)
        return _page_getter.get_page()

    def get_page_getting_strategy(self, **kwargs):
        """Override this method to set the page getting strategy"""
        return SimplePage(
            self.get_search_url, kwargs
        )

    def get_search_url(self, game):
        """Override this method to set the url getter callback"""
        pass

    def _parse_price(self, response):
        game_boxes = response.xpath(self.game_box_xpath)
        game_box_list = GameBoxList(*game_boxes)
        game_data = self.data_extractor.extract_data(game_box_list)
        iterator = game_data.make_iterator()

        there_is_items_in_list = not iterator.is_done()

        while there_is_items_in_list:
            current_index = iterator.get_index()
            current_item = game_data.get_item_at(current_index)
            yield from self._validate_data(current_item, self.search)

            iterator.next()
            there_is_items_in_list = not iterator.is_done()

    def _validate_data(self, game: Game, search: Search):
        game_name = game.get_name()
        has_name = len(game_name) > 0

        game_price = game.get_price()
        has_price = game_price > 0.00

        game_link = game.get_link()
        has_link = len(game_link) > 0

        if has_name and has_price and has_link:
            game_link = self.validate_link(game_link)
            game.set_link(game_link)

            yield {
                'game': game,
                'search': search,
            }

    def validate_link(self, link):
        return link
