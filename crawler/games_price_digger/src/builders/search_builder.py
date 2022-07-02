from games_price_digger.src.components.search import Search


class SearchBuilder:
    def set_game(self, game):
        self._game = game
        return self

    def set_store(self, store: str):
        self._store = store
        return self

    def build(self):
        return Search(
            self._game,
            self._store
        )
