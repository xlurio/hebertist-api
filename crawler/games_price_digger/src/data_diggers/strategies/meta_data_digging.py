from games_price_digger.src.builders.meta_data_settings_builder import \
    MetaDataSettingsBuilder
from . import DiggingStrategy


class MetaDataDigging(DiggingStrategy):

    def make_settings_builder(
        self, item_title_xpath: str, item_score_xpath: str,
        item_image_xpath: str
    ) -> MetaDataSettingsBuilder:
        builder = MetaDataSettingsBuilder()
        builder.set_item_title_xpath(item_title_xpath)
        builder.set_item_score_xpath(item_score_xpath)
        builder.set_item_image_xpath(item_image_xpath)
        return builder

    def dig_data(self, settings) -> dict:
        self.box = settings.get_item_box()

        item_title_xpath = settings.get_item_title_xpath()
        item_title = self._make_item_title(item_title_xpath)

        item_score_xpath = settings.get_item_score_xpath()
        item_score = self._make_item_score(item_score_xpath)

        item_image_xpath = settings.get_item_image_xpath()
        item_image = self._make_item_image(item_image_xpath)

        return {
            'name': item_title,
            'score': item_score,
            'image': item_image,
        }

    def _make_item_title(self, item_title_xpath) -> str:
        item_title_element = self.box.xpath(item_title_xpath)
        item_title = item_title_element.get()
        parsed_item_title = str(item_title)
        return parsed_item_title.strip()

    def _make_item_score(self, item_score_xpath) -> int:
        item_score_element = self.box.xpath(item_score_xpath)
        item_score = item_score_element.get()
        return self._parse_score(item_score)

    def _parse_score(self, score):
        try:
            return int(score)
        except ValueError:
            return 0

    def _make_item_image(self, item_image_xpath) -> str:
        item_image_element = self.box.xpath(item_image_xpath)
        item_image = item_image_element.get()
        parsed_item_image = str(item_image)
        return parsed_item_image.strip()
