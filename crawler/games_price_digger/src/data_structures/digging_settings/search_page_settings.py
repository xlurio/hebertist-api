from scrapy import Selector
from . import DiggingSettings


class SearchPageSettings(DiggingSettings):

    def __init__(self, item_box: Selector, item_title_xpath: str,
                 item_link_xpath: str) -> None:
        self._item_box = item_box
        self._item_title_xpath = f'.//descendant::{item_title_xpath}/text()'
        self._item_link_xpath = f'.//{item_link_xpath}'

    def get_item_box(self):
        return self._item_box

    def get_item_title_xpath(self):
        return self._item_title_xpath

    def get_item_link_xpath(self):
        return self._item_link_xpath
