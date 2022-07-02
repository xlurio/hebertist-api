# import urllib.parse
# import pandas as pd

# from games_price_digger.src.adapters import GameDataFrameAdapter
# from games_price_digger.src.builders.game_builder import GameBuilder
# from games_price_digger.src.builders.simple_extraction_builder import SimpleExtractionBuilder
# from games_price_digger.src.builders.search_builder import SearchBuilder
# from games_price_digger.src.data_diggers.data_digger import DataDigger
# from games_price_digger.src.data_diggers.strategies.price_digging_strategies.real_number_digging import RealNumberDigging
# from games_price_digger.src.data_diggers.strategies.search_page_digging import SearchPageDigging
# from games_price_digger.src.data_getters.page_data_extractor import PageDataExtractor
# from games_price_digger.src.data_getters.strategies import simple_extraction
# from games_price_digger.src.data_getters.strategies.simple_extraction import SimpleExtraction
# from games_price_digger.src.game_name_getter import GameNamesGetter
# from games_price_digger.src.lists import GameBoxList
# from games_price_digger.src.page_getters.page_getter import PageGetter
# from games_price_digger.src.page_getters.strategies import SimplePage

# from .utils.price.price_getters.price_getter import RealNumberPriceGetter
# from scrapy import Spider
# from core.models import GameModel


# class EpicPriceParser(Spider):
#     name = 'epic_price'

#     _store_name = 'Epic Games'
#     _game_box_xpath = 'div[@class="css-13ku56z"]'
#     _game_title_xpath = 'div[@class="css-1h2ruwl"]'
#     _game_price_xpath = 'span[@class="css-z3vg5b"]'
#     _next_page_link = 'a[@class="css-1ns6940"]'

#     _games_in_database = GameModel.objects.all().values()
#     _game_dataframe = pd.DataFrame(_games_in_database)
#     _game_data = GameDataFrameAdapter(_game_dataframe, 'name')
#     _name_getter = GameNamesGetter()

#     _page_getting_strategy = SimplePage()
#     _page_getter = PageGetter(_page_getting_strategy)

#     _price_digging_strategy = RealNumberDigging(_game_price_xpath)
#     _digging_strategy = SearchPageDigging(_price_digging_strategy)
#     _data_digger = DataDigger(_digging_strategy)

#     _simple_extraction_builder = SimpleExtractionBuilder()
#     _data_extractor = PageDataExtractor()

#     _search_builder = SearchBuilder().set_store(_store_name)

#     allowed_domains = ['store.epicgames.com']
#     start_urls = ['https://store.epicgames.com/']

#     def _get_search_url(self, game):
#         encoded_name = urllib.parse.quote(game)
#         return (f'{self.start_urls[0]}browse?q={encoded_name}&' +
#                 'sortBy=relevancy&sortDir=DESC&category=Game&' +
#                 'count=40&start=0')

#     def parse(self, response, **kwargs):
#         self._page_getter.set_url_getter_callback(self._get_search_url)

#         for game in self.name_getter.yield_names():
#             url_getter_parameters = {'game': game}
#             self._page_getter.set_url_getter_parameters(
#                 url_getter_parameters
#             )

#             response = self._page_getter.get_page()

#             self._search_builder.set_game(game)
#             search = self._search_builder.build()

#             self._simple_extraction_builder.set_response(response)
#             self._simple_extraction_builder.set_search(search)
#             self._simple_extraction_builder.set_data_digger(self._data_digger)
#             simple_extraction = self._simple_extraction_builder.build()
#             self._data_extractor.set_strategy(simple_extraction)

#             game_boxes = response.xpath(self._game_box_xpath)
#             game_box_list = GameBoxList(game_boxes)

#             for game in self._data_extractor.extract_data(game_box_list):
#                 yield {
#                     'game': game.get_name(),
#                     'price': game.get_price(),
#                 }
