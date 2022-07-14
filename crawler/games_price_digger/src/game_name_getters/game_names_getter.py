from games_price_digger.src.adapters import GameDataFrameAdapter


class GameNamesGetter:

    def yield_names(self, game_data: GameDataFrameAdapter):
        yield from game_data.yield_game_names()
