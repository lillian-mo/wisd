import pandas as pd
from pandas import DataFrame
import py_ball

def load_game(data: str) -> DataFrame:
    return pd.read_json(data, lines=True)

game2 = load_game("0042100302_events.jsonl")
game2 = game2.query("eventType == 'DRIBBLE'")
print(game2)
