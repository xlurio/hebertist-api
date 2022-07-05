import math

from games_price_digger.src.components.game import Game


class FoundGame(Game):

    def __init__(self, name: str, price: float, link: str):
        self._name = name
        self._price = price
        self._link = link

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_link(self):
        return self._link

    def set_link(self, link):
        self._link = link

    def get_data(self) -> dict:
        return {
            'name': self._name,
            'price': self._price,
            'link': self._link,
        }

    def __eq__(self, __o: object) -> bool:
        is_name_equal = self._name == __o.get_name()
        is_price_equal = math.isclose(self._price, __o.get_price())
        is_link_equal = self._link == __o.get_link()
        return is_name_equal and is_price_equal and is_link_equal

    def __lt__(self, other):
        return self._name < other.get_name()

    def __str__(self) -> str:
        return (
            '{\n'
            f'\tname: {self._name},\n'
            f'\tprice: {self._price},\n'
            f'\tlink: {self._link},\n'
            '}'
        )
