import pandas as pd
import unittest
from games_price_digger.src.adapters import GameDataFrameAdapter


class GameDataFrameAdapterTests(unittest.TestCase):

    def test_yield_game_names(self):
        """Test yield the game names"""
        game_data = {
            'name': ['Tetris', 'Pinball'],
            'score': [15453451, 5351531],
        }
        game_data_frame = pd.DataFrame(game_data)
        game_data_frame_adapter = GameDataFrameAdapter(
            dataframe=game_data_frame,
            game_name_column='name'
        )
        result = [name for name in game_data_frame_adapter.yield_game_names()]
        expected_result = game_data['name']
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
