import pandas as pd
from pandas import DataFrame

def load_game(game_id: str) -> DataFrame:
    df_e = pd.read_json(f"{game_id}_events.jsonl", lines=True)
    df_t = pd.read_json(f"{game_id}_tracking.jsonl", lines=True).drop_duplicates(subset=['gameClock','period'])

    return df_e.merge(df_t, how='inner', on=['gameClock', 'period']).filter\
                    (items=['eventType','shotClock_x','gameClock','period','ball'])


def game_evs(df: DataFrame, event_id: int, oord: str='none') -> DataFrame:

    if oord == 'o':
        new_df = df.query(f"eventType == '{evs[event_id]}' and shotClock_x != 24.0")
    elif oord == 'd':
        new_df = df.query(f"eventType == '{evs[event_id]}' and shotClock_x == 24.0")
    else:
        new_df = df.query(f"eventType == '{evs[event_id]}'")
    
    new_coords = pd.DataFrame(new_df.pop('ball').tolist(), index=new_df.index, columns = ['x','y','z'])
    final_df = pd.concat([new_df, new_coords.reindex(game2.index)], axis=1).dropna()

    return final_df


game2 = load_game("0042100302")
print(game2)
evs = game2.eventType.unique().tolist()
#offensive rebounds testing
game2_oreb = game_evs(game2, evs.index('REB'), 'o')
game2_dreb = game_evs(game2, evs.index('REB'), 'd')
print(game2_oreb)
print(game2_dreb)