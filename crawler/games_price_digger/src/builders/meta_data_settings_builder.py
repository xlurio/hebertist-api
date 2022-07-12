from games_price_digger.src.builders.digging_settings_builder import DiggingSettingsBuilder
from games_price_digger.src.data_structures.digging_settings.meta_data_settings import MetaDataSettings


class MetaDataSettingsBuilder(DiggingSettingsBuilder):

    def set_item_box(self, item_box):
        self._item_box = item_box
        return self

    def set_item_title_xpath(self, item_title_xpath):
        self._item_title_xpath = item_title_xpath
        return self

    def set_item_score_xpath(self, item_score_xpath):
        self._item_score_xpath = item_score_xpath
        return self

    def set_item_image_xpath(self, item_image_xpath):
        self._item_image_xpath = item_image_xpath
        return self

    def build(self):
        return MetaDataSettings(
            self._item_box, self._item_title_xpath, self._item_score_xpath,
            self._item_image_xpath
        )
