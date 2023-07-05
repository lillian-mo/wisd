import pandas as pd
from pandas import DataFrame

def load_game(data: str) -> DataFrame:
    return pd.read_json(data, lines=True)
