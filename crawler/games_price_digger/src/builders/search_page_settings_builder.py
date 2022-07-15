from scrapy import Selector
from games_price_digger.src.builders.digging_settings_builder import \
    DiggingSettingsBuilder
from games_price_digger.src.data_structures.digging_settings \
    .search_page_settings import SearchPageSettings


class SearchPageSettingsBuilder(DiggingSettingsBuilder):

    def set_item_box(self, item_box: Selector):
        self._item_box = item_box
        return self

    def set_item_title_xpath(self, item_title_xpath: str):
        self._item_title_xpath = item_title_xpath
        return self

    def set_item_link_xpath(self, item_link_xpath: str):
        self._item_link_xpath = item_link_xpath
        return self

    def build(self):
        return SearchPageSettings(
            self._item_box,
            self._item_title_xpath,
            self._item_link_xpath
        )
