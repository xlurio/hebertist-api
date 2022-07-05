from games_price_digger.src.builders.digging_settings_builder import DiggingSettingsBuilder
from games_price_digger.src.components.search import Search
from games_price_digger.src.data_diggers.data_digger import DataDigger
from games_price_digger.src.data_getters.strategies.simple_extraction import SimpleExtraction


class SimpleExtractionBuilder:

    def set_settings_builder(self, settings_builder: DiggingSettingsBuilder):
        self._settings_builder = settings_builder

    def set_search(self, search: Search):
        self._search = search
        return self

    def set_data_digger(self, data_digger: DataDigger):
        self._data_digger = data_digger
        return self

    def build(self):
        return SimpleExtraction(
            digging_settings_builder=self._settings_builder,
            search=self._search,
            data_digger=self._data_digger,
        )
