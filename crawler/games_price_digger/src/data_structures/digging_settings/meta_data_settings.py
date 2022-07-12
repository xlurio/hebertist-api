from scrapy import Selector

from games_price_digger.src.components.meta_game import MetaGame
from . import DiggingSettings


class MetaDataSettings(DiggingSettings):

    def __init__(self, item_box: Selector, item_title_xpath: str,
                 item_score_xpath: str, item_image_xpath: str):
        self._item_box = item_box
        self._item_title_xpath = f'.//descendant::{item_title_xpath}/text()'
        self._item_score_xpath = f'.//descendant::{item_score_xpath}/text()'
        self._item_image_xpath = f'.//descendant::{item_image_xpath}/@src'

    def get_item_box(self):
        return self._item_box

    def get_item_title_xpath(self):
        return self._item_title_xpath

    def get_item_score_xpath(self):
        return self._item_score_xpath

    def get_item_image_xpath(self):
        return self._item_image_xpath

    def make_item(self, **kwargs):
        return MetaGame(**kwargs)
