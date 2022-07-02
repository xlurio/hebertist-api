import pandas as pd


class GameDataFrameAdapter:

    def __init__(self, dataframe: pd.DataFrame, game_name_column: str):
        game_name_series = dataframe[game_name_column]
        self._game_names = list(game_name_series)

    def yield_game_names(self):
        for name in self._game_names:
            yield name

    def get_game_names(self):
        return self._game_names
