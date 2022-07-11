import time
import scrapy
from games_price_digger.src.builders.simple_extraction_builder import SimpleExtractionBuilder
from games_price_digger.src.components.meta_game import MetaGame
from games_price_digger.src.data_diggers.data_digger import DataDigger
from games_price_digger.src.data_diggers.strategies.meta_data_digging import MetaDataDigging
from games_price_digger.src.data_getters.page_data_extractor import PageDataExtractor
from games_price_digger.src.lists.game_box_list import GameBoxList
from games_price_digger.src.lists.meta_game_list import MetaGameList


class GamesMetascoreSpider(scrapy.Spider):
    """Spider that gets the names and scores of the PC games in Metacritics"""
    _testing_html_file = None
    _data_extractor_class = PageDataExtractor
    _testing = False

    name = 'games_metascore'

    game_box_xpath = (
        'div[starts-with(@class, "browse_list_wrapper")]' +
        '/descendant::tr[not(@class="spacer")]'
    )
    game_title_xpath = 'h3'
    game_score_xpath = 'div[starts-with(@class, "metascore_w")]'
    game_image_xpath = 'img'
    next_page_link_xpath = 'a[@rel="next"]'

    extraction_strategy_builder = SimpleExtractionBuilder()

    allowed_domains = ['www.metacritic.com']
    start_urls = [
        'https://www.metacritic.com/browse/games/score/metascore/all/pc/'
    ]

    def __init__(self):
        self.game_box_xpath = f'//{self.game_box_xpath}'
        self._set_data_digger()

    def _set_data_digger(self):
        self.set_digging_strategy()
        self._data_digger = DataDigger(self.digging_strategy)

    def set_digging_strategy(self):
        """Override this method to set digging strategy"""
        self.digging_strategy = MetaDataDigging()

    def parse(self, response, **kwargs):
        if kwargs.get('testing'):
            self._testing = True

        game_box_elements = response.xpath(self.game_box_xpath)
        game_box_list = GameBoxList(*game_box_elements)
        yield from self._iterate_game_box_list(game_box_list)

        # Go to the next page
        next_page_link = self._get_next_page_link(response)

        if next_page_link and not self._testing:
            yield response.follow(
                url=next_page_link,
                callback=self.parse
            )

    def _get_next_page_link(self, response):
        next_page_link_element = response.xpath(
            f'//{self.next_page_link_xpath}/@href'
        )
        next_page_link = next_page_link_element.get()
        next_page_link = str(next_page_link)
        return next_page_link.strip()

    def _iterate_game_box_list(self, game_box_list: GameBoxList):
        self._set_data_extrator()
        game_list = self._data_extractor.extract_data(game_box_list)
        iterator = game_list.make_iterator()

        while not iterator.is_done():
            current_index = iterator.get_index()
            current_item = game_list.get_item_at(current_index)
            yield from self._validate_item(current_item)
            time.sleep(3)

            iterator.next()

    def _validate_item(self, item):
        game_name = item.get_name()
        there_is_name = len(game_name) > 0

        game_score = item.get_score()
        there_is_score = game_score > 0

        if there_is_name and there_is_score:
            yield {
                'game_metadata': item
            }

    def _set_data_extrator(self):
        search_items_list = MetaGameList()
        self.extraction_strategy_builder.set_search_items_list(
            search_items_list
        )

        settings_builder = self.make_settings_builder()
        self.extraction_strategy_builder.set_settings_builder(settings_builder)

        self.extraction_strategy_builder.set_data_digger(self._data_digger)

        extraction_strategy = self.extraction_strategy_builder.build()
        self._data_extractor = self._data_extractor_class(extraction_strategy)

    def make_settings_builder(self):
        """Override this method to set the digging settings"""
        return self.digging_strategy.make_settings_builder(
            self.game_title_xpath,
            self.game_score_xpath,
            self.game_image_xpath,
        )
