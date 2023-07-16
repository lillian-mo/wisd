import pandas as pd
from pandas import DataFrame
import py_ball

def load_game(data: str) -> DataFrame:
    return pd.read_json(data, lines=True)

def game_evs(df: DataFrame, event_id: int) -> DataFrame:
    new_df = df.query(f"eventType == '{evs[event_id]}'")
    return new_df

game2_events = load_game("0042100302_events.jsonl")
game2_track = load_game("0042100302_tracking.jsonl").drop_duplicates(subset=['gameClock', 'period'])
game2_merged = game2_events.merge(game2_track, how='inner', on=['gameClock', 'period'])
game2 = game2_merged.filter(items=["eventType", "shotClock_x", "gameClock", "period", "ball"])
print(game2)
evs = game2.eventType.unique().tolist()
print(evs)
game2_oreb = game_evs(game2, 4).query(f"shotClock_x != 24.0").drop('eventType', axis=1)
game2_dreb = game_evs(game2, 4).query(f"shotClock_x == 24.0").drop('eventType', axis=1)
print(game2_oreb)
print(game2_dreb)