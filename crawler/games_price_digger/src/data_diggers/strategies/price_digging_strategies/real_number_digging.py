from numpy import character
from . import PriceDiggingStrategy


class RealNumberDigging(PriceDiggingStrategy):

    def __init__(self, price_xpath: str):
        self._price_xpath = f'.//descendant::{price_xpath}/text()'

    def dig_data(self, element):
        price_element = element.xpath(self._price_xpath)
        scraped_data = price_element.getall()
        scraped_price = self._clean_data(scraped_data)
        return self._format(scraped_price)

    def _clean_data(self, data):
        for item in data:
            if '$' in item:
                return item
        return ''

    def _format(self, price: str) -> float:
        numbers_only_price = self._extract_numbers(price)
        price_in_usa_notation = self._european_to_usa(numbers_only_price)

        try:
            return float(price_in_usa_notation)
        except ValueError:
            return 0.00

    def _extract_numbers(self, source_to_extract: str) -> str:
        valid_characters = '1234567890,.'
        extracted_characters = [
            self._validate_character(char) for char in source_to_extract
        ]
        return ''.join(extracted_characters)

    def _validate_character(self, char: str) -> str:
        valid_characters = '1234567890,.'
        if char in valid_characters:
            return char
        return ''

    def _european_to_usa(self, decimal_number: str) -> str:
        has_comma = ',' in decimal_number
        has_dot = '.' in decimal_number
        if has_dot and has_comma:
            decimal_number = self._check_if_dot_is_before_comma(decimal_number)
            decimal_number = self._check_if_comma_is_before_dot(decimal_number)
        return decimal_number.replace(',', '.')

    def _check_if_dot_is_before_comma(self, decimal_number: str) -> str:
        if self._is_dot_before_comma(decimal_number):
            decimal_number = self._remove_dot(decimal_number)
        return decimal_number

    def _check_if_comma_is_before_dot(self, decimal_number: str) -> str:
        if not self._is_dot_before_comma(decimal_number):
            decimal_number = self._replace_comma(decimal_number)
        return decimal_number

    def _is_dot_before_comma(self, decimal_number: str) -> bool:
        index_of_comma = decimal_number.index(',')
        index_of_dot = decimal_number.index('.')
        return index_of_dot < index_of_comma

    def _remove_dot(self, decimal_number: str) -> str:
        return decimal_number.replace('.', '')

    def _replace_comma(self, decimal_number):
        return decimal_number.replace(',', '.')
