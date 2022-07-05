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
        box = settings.get_item_box()

        item_title_xpath = settings.get_item_title_xpath()
        item_title_element = box.xpath(item_title_xpath)
        item_title = item_title_element.get()
        parsed_item_title = str(item_title)
        stripped_item_title = parsed_item_title.strip()

        item_link_xpath = settings.get_item_link_xpath()
        item_link_element = box.xpath(item_link_xpath)
        item_link = item_link_element.get()
        parsed_item_link = str(item_link)
        stripped_item_link = parsed_item_link.strip()

        item_price = self._strategy.dig_data(box)

        return {
            'name': stripped_item_title,
            'price': item_price,
            'link': stripped_item_link,
        }
