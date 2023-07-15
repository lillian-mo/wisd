import pandas as pd
from pandas import DataFrame
import py_ball

def load_game(data: str) -> DataFrame:
    return pd.read_json(data, lines=True)

def game_evs(df: DataFrame, event_id: int) -> DataFrame:
    new_df = df.query(f"eventType == '{evs[event_id]}'")
    new_df = new_df.filter(items=["eventType", "shotClock", "gameClock", "playerId", "period"])
    return new_df

game2 = load_game("0042100302_events.jsonl")
print(game2)
evs = game2.eventType.unique().tolist()
print(evs)
game2_oreb = game_evs(game2, 4).query(f"shotClock != 24.0")
game2_dreb = game_evs(game2, 4).query(f"shotClock == 24.0")
game2_touch = game_evs(game2, 0)
print(game2_oreb)
print(game2_dreb)
print(game2_touch)