from operator import indexOf
import stat
from urllib import response

from games_price_digger.src.data_diggers.strategies.price_digging_strategies.price_digging_strategy import PriceDiggingStrategy
from . import DiggingStrategy
from scrapy.http import Response


class SearchPageDigging(DiggingStrategy):

    def set_strategy(self, strategy: PriceDiggingStrategy) -> None:
        self._strategy = strategy

    def dig_data(self, **digging_parameters) -> dict:
        self._check_for_parameters(digging_parameters)

        box = digging_parameters.get('item_box')

        item_title_xpath = digging_parameters.get('item_title_xpath')
        item_title_xpath = f'.//descendant::{item_title_xpath}/text()'

        item_title_element = box.xpath(item_title_xpath)
        item_title = item_title_element.get()
        parsed_item_title = str(item_title)
        stripped_item_title = parsed_item_title.strip()

        item_link_xpath = digging_parameters.get('item_link_xpath')
        item_link_xpath = f'.//{item_link_xpath}'

        item_link_element = box.xpath(item_link_xpath)
        item_link = item_link_element.get()
        parsed_item_link = str(item_link)
        stripped_item_link = parsed_item_link.strip()

        if self._strategy:
            item_price = self._strategy.dig_data(box)
        else:
            raise ValueError('A price digging strategy must be set')

        return {
            'name': stripped_item_title,
            'price': item_price,
            'link': stripped_item_link,
        }

    def _check_for_parameters(self, parameters: dict) -> None:
        parameters_needed = [
            'item_box', 'item_title_xpath', 'item_link_xpath'
        ]
        parameters_passed = [
            parameters.get(param) for param in parameters_needed
        ]
        was_parameters_passed = [
            value != None for value in parameters_passed
        ]

        if False in was_parameters_passed:
            not_passed_parameter_index = \
                self._get_not_passed_parameter_index(was_parameters_passed)
            not_passed_parameter = parameters_needed[not_passed_parameter_index]

            raise ValueError(
                f'{not_passed_parameter} parameter was not passed'
                f'\nthe values passed was {parameters}'
            )

    @staticmethod
    def _get_not_passed_parameter_index(was_parameters_passed: list):
        return indexOf(was_parameters_passed, False)
