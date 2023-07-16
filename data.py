import pandas as pd
from pandas import DataFrame

def load_game(game_id: str) -> DataFrame:
    df_e = pd.read_json(f"{game_id}_events.jsonl", lines=True)
    df_t = pd.read_json(f"{game_id}_tracking.jsonl", lines=True).drop_duplicates(subset=['gameClock','period'])

    return df_e.merge(df_t, how='inner', on=['gameClock', 'period']).filter\
                    (items=['eventType','shotClock_x','gameClock','period','ball'])

def mult_games(games: list) -> DataFrame:
    df = load_game(games[0])
    for i in games[1:]:
        df = pd.concat(objs=[df, load_game(i)], ignore_index=True)

    return df

def game_evs(df: DataFrame, event: str, oord: str='none') -> DataFrame:

    if oord == 'o':
        new_df = df.query(f"eventType == '{event}' and shotClock_x != 24.0")
    elif oord == 'd':
        new_df = df.query(f"eventType == '{event}' and shotClock_x == 24.0")
    else:
        new_df = df.query(f"eventType == '{event}'")
    
    new_coords = pd.DataFrame(new_df.pop('ball').tolist(), index=new_df.index, columns = ['x','y','z'])
    final_df = pd.concat([new_df, new_coords.reindex(new_df.index)], axis=1).dropna()

    return final_df