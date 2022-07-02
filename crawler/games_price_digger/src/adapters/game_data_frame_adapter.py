import pandas as pd


class GameDataFrameAdapter:

    def __init__(self, dataframe: pd.DataFrame, game_name_column: str):
        self._game_name_column = game_name_column
        self._adapt_dataframe(dataframe)

    def _adapt_dataframe(self, dataframe):
        if len(dataframe.index) <= 0:
            dataframe = pd.DataFrame({
                self._game_name_column: ['nan']
            })
        game_name_series = dataframe[self._game_name_column]
        self._game_names = list(game_name_series)

    def yield_game_names(self):
        for name in self._game_names:
            yield name

    def get_game_names(self):
        return self._game_names
