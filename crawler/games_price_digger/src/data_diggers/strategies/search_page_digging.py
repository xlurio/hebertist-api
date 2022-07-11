from games_price_digger.src.builders.search_page_settings_builder import SearchPageSettingsBuilder
from games_price_digger.src.data_diggers.strategies.price_digging_strategies.price_digging_strategy import PriceDiggingStrategy
from games_price_digger.src.data_structures.digging_settings.search_page_settings import SearchPageSettings
from . import DiggingStrategy


class SearchPageDigging(DiggingStrategy):

    def __init__(self, strategy: PriceDiggingStrategy) -> None:
        self._strategy = strategy

    def make_settings_builder(
        self, item_title_xpath, item_link_xpath
    ) -> SearchPageSettingsBuilder:
        builder = SearchPageSettingsBuilder()
        builder.set_item_title_xpath(item_title_xpath)
        builder.set_item_link_xpath(item_link_xpath)
        return builder

    def dig_data(self, settings: SearchPageSettings) -> dict:
        self.box = settings.get_item_box()

        item_title_xpath = settings.get_item_title_xpath()
        item_title = self._make_item_title(item_title_xpath)

        item_link_xpath = settings.get_item_link_xpath()
        item_link = self._make_item_link(item_link_xpath)

        item_price = self._strategy.dig_data(self.box)

        return {
            'name': item_title,
            'price': item_price,
            'link': item_link,
        }

    def _make_item_title(self, item_title_xpath):
        item_title_element = self.box.xpath(item_title_xpath)
        item_title = item_title_element.get()
        parsed_item_title = str(item_title)
        return parsed_item_title.strip()

    def _make_item_link(self, item_link_xpath):
        item_link_element = self.box.xpath(item_link_xpath)
        item_link = item_link_element.get()
        parsed_item_link = str(item_link)
        return parsed_item_link.strip()
