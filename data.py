import pandas as pd
from pandas import DataFrame
from py_ball import playbyplay
from typing import Union
import numpy as np

HEADERS = {'Connection': 'keep-alive',
           'Host': 'stats.nba.com',
           'Origin': 'http://stats.nba.com',
           'Upgrade-Insecure-Requests': '1',
           'Referer': 'stats.nba.com',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token': 'true',
           'Accept-Language': 'en-US,en;q=0.9',
           "X-NewRelic-ID": "VQECWF5UChAHUlNTBwgBVw==",
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)' +\
                         ' AppleWebKit/537.36 (KHTML, like Gecko)' + \
                         ' Chrome/81.0.4044.129 Safari/537.36'}

event_dict = {
    1: 'SHOT',
    2: 'SHOT',
    3: 'FT',
    4: 'REB',
    5: 'TO',
    6: 'FOUL',
    7: 'VIO',
    8: 'SUB',
    9: 'TMO',
    10: 'JB'
}


def load_game(game_id: str) -> DataFrame:
    df_e = pd.read_json(f"./games/{game_id}/{game_id}_events.jsonl", lines=True)
    df_t = pd.read_json(f"./games/{game_id}/{game_id}_tracking.jsonl", lines=True).drop_duplicates(subset=['gameClock','period'])
    plays = playbyplay.PlayByPlay(headers=HEADERS,
                              endpoint='playbyplayv2',
                              game_id=game_id)
    play_df = pd.DataFrame(plays.data['PlayByPlay'])
    play_df = play_df.filter(items=['EVENTNUM', 'EVENTMSGTYPE', 'GAME_ID', 'PLAYER1_TEAM_NICKNAME'])
    play_df['event'] = play_df['EVENTMSGTYPE'].map(event_dict)

    e_and_t = df_e.merge(df_t, how='inner', on=['gameClock', 'period']).filter\
                    (items=['gameId', 'eventType','shotClock_x','gameClock','period','ball', 'pbpId'])
    final_df = e_and_t.merge(play_df, left_on=['eventType','pbpId'], right_on=['event','EVENTNUM'], how='inner').\
                    rename(columns={'PLAYER1_TEAM_NICKNAME': 'team'}).drop(columns=['event', 'pbpId'])
       
    return final_df


def mult_games(games: list) -> DataFrame:
    df = load_game(games[0])
    for i in games[1:]:
        df = pd.concat(objs=[df, load_game(i)], ignore_index=True)

    return df

def game_evs(df: DataFrame, events: Union[list, int], team: str='none', oord: str='none') -> DataFrame:

    if type(events) == list:
        string = f"EVENTMSGTYPE == {events[0]}"
        for i in events:
            string = f"{string} or EVENTMSGTYPE == {i}"
        new_df = df.query(string)
    else:
        new_df = df.query(f"EVENTMSGTYPE == {events}")

    
    if oord == 'o':
        new_df = new_df.query(f"shotClock_x != 24.0")
    if oord == 'd':
        new_df = new_df.query(f"shotClock_x == 24.0")  
    if team != 'none':
        new_df = new_df.query(f"team == '{team}'") 
    

    new_coords = pd.DataFrame(new_df.pop('ball').tolist(), index=new_df.index, columns = ['x','y','z'])
    combined = pd.concat([new_df, new_coords.reindex(new_df.index)], axis=1).dropna()

    return combined.drop(columns=['gameId'])
    return new_df

def in_ranges(time: float, period: int, ranges: list) -> bool:
    time_int = int(time * 100)
    for i in ranges:
        if time_int >= i[0] and time_int <= i[1] and period == i[2]:
            return True
    
    return False

def high_danger(df: DataFrame, rebs: DataFrame, shots: DataFrame) -> DataFrame:
    reb_ranges = []
    shot_copy = shots
    n = rebs.gameClock.values.tolist()
    p = rebs.period.values.tolist()
    for i in range(len(n)- 1):
        num = n[i]
        reb_ranges.append([int(num * 100) - 1000, int(num * 100), p[i]])
    
    shot_copy['inRange'] = shot_copy.apply(lambda x: in_ranges(x.gameClock, x.period, reb_ranges), axis=1)
    shot_copy = shot_copy.query('inRange == True')
    shot_copy = shot_copy.drop(columns=['inRange'])

    return shot_copy