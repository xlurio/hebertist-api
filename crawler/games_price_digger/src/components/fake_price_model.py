from games_price_digger.src.components.fake_model import FakeModel


class FakePriceModel:
    price = 0.0
    link = ''

    objects = None

    def __init__(self, game: FakeModel, store: FakeModel, price: float,
                 link: str):
        self.game = game
        self.store = store
        self.price = price
        self.link = link
        self._saved = False

    def save(self):
        self._saved = True

    def __str__(self):
        return (
            '{\n' +
            f'\tname: {self.game.name},\n' +
            f'\tstore: {self.store.name},\n' +
            f'\tprice: {str(self.price)}\n' +
            f'\tlink: {self.link}\n' +
            '}'
        )
