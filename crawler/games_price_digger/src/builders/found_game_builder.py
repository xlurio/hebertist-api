from games_price_digger.src.components.found_game import FoundGame


class FoundGameBuilder:
    def set_name(self, name):
        self._name = name
        return self

    def set_price(self, price):
        self._price = price
        return self

    def set_link(self, link):
        self._link = link
        return self

    def build(self):
        return FoundGame(self._name, self._price, self._link)
