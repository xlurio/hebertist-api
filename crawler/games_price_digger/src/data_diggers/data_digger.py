from games_price_digger.src.data_diggers.strategies import DiggingStrategy


class DataDigger:

    def __init__(self, strategy: DiggingStrategy):
        self._strategy = strategy

    def dig_data(self, **digging_parameters):
        return self._strategy.dig_data(**digging_parameters)
