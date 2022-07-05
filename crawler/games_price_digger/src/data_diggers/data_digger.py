from games_price_digger.src.data_diggers.strategies import DiggingStrategy
from games_price_digger.src.data_structures.digging_settings.digging_settings import DiggingSettings


class DataDigger:

    def __init__(self, strategy: DiggingStrategy):
        self._strategy = strategy

    def dig_data(self, settings: DiggingSettings):
        return self._strategy.dig_data(settings)
