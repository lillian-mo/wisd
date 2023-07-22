import pandas as pd
from pandas import DataFrame
import teams

def load_game(game_id: str) -> DataFrame:
    df_e = pd.read_json(f"./games/{game_id}/{game_id}_events.jsonl", lines=True)
    df_t = pd.read_json(f"./games/{game_id}/{game_id}_tracking.jsonl", lines=True).drop_duplicates(subset=['gameClock','period'])

    e_and_t = df_e.merge(df_t, how='inner', on=['gameClock', 'period']).filter\
                    (items=['gameId', 'eventType','shotClock_x','gameClock','period','ball'])\
    
    return e_and_t
    


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
    combined = pd.concat([new_df, new_coords.reindex(new_df.index)], axis=1).dropna()
    
    combined['gameId'] = combined['gameId'].astype(str)
    teams.all_games['game'] = teams.all_games['game'].astype(str)
    combined['gameId'] = combined['gameId'].map(teams.all_games.set_index('game')['homeTeam'])

    return combined