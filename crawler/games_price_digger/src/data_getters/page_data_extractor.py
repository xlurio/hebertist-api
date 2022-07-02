from games_price_digger.src.data_getters.strategies.extraction_strategy import ExtractionStrategy
from games_price_digger.src.lists.game_box_list import GameBoxList


class PageDataExtractor:

    def __init__(self, strategy=None):
        self._strategy = strategy

    def extract_data(self, game_box_list: GameBoxList):
        if self._strategy:
            return self._strategy.extract_data(game_box_list)

        raise ValueError('Strategy was not set')

    def set_strategy(self, strategy: ExtractionStrategy):
        self._strategy = strategy
