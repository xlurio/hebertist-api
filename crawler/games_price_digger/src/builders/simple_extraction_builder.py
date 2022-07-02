from games_price_digger.src.data_getters.strategies.simple_extraction import SimpleExtraction


class SimpleExtractionBuilder:

    def set_item_title_xpath(self, item_title_xpath: str):
        self._item_title_xpath = item_title_xpath
        return self

    def set_item_link_xpath(self, item_link_xpath):
        self._item_link_xpath = item_link_xpath
        return self

    def set_search(self, search):
        self._search = search
        return self

    def set_data_digger(self, data_digger):
        self._data_digger = data_digger
        return self

    def build(self):
        return SimpleExtraction(
            item_title_xpath=self._item_title_xpath,
            item_link_xpath=self._item_link_xpath,
            search=self._search,
            data_digger=self._data_digger,
        )
