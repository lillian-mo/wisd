import pandas as pd
from pandas import DataFrame
import py_ball

def load_game(data: str) -> DataFrame:
    return pd.read_json(data, lines=True)

def game_rebs(df: DataFrame, oord: str) -> DataFrame:
    if oord == "o":
        new_df = df.query(f"eventType == 'REB' and shotClock == 24.0")
    else:
        new_df = df.query(f"eventType == 'REB' and shotClock != 24.0")
    new_df = new_df.filter(items=["eventType", "shotClock", "gameClock", "playerId", "period"])
    return new_df


game2 = load_game("0042100302_events.jsonl")
game2_oreb = game_rebs(game2, 'o')
game2_dreb = game_rebs(game2, 'd')
print(game2_oreb)
print(game2_dreb)