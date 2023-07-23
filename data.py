import pandas as pd
from pandas import DataFrame
from py_ball import playbyplay

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


def load_game(game_id: str) -> DataFrame:
    df_e = pd.read_json(f"./games/{game_id}/{game_id}_events.jsonl", lines=True)
    df_t = pd.read_json(f"./games/{game_id}/{game_id}_tracking.jsonl", lines=True).drop_duplicates(subset=['gameClock','period'])
    plays = playbyplay.PlayByPlay(headers=HEADERS,
                              endpoint='playbyplayv2',
                              game_id=game_id)
    play_df = pd.DataFrame(plays.data['PlayByPlay']).filter\
        (items=['EVENTNUM', 'PERIOD', 'GAME_ID', 'PLAYER1_TEAM_NICKNAME'])

    e_and_t = df_e.merge(df_t, how='inner', on=['gameClock', 'period']).filter\
                    (items=['gameId', 'eventType','shotClock_x','gameClock','period','ball', 'pbpId'])
    final_df = e_and_t.merge(play_df, left_on='pbpId', right_on='EVENTNUM')
       
    return final_df


def mult_games(games: list) -> DataFrame:
    df = load_game(games[0])
    for i in games[1:]:
        df = pd.concat(objs=[df, load_game(i)], ignore_index=True)

    return df

def game_evs(df: DataFrame, event: str, team: str, oord: str='none') -> DataFrame:

    if oord == 'o':
        new_df = df.query(f"eventType == '{event}' and shotClock_x != 24.0 and PLAYER1_TEAM_NICKNAME == '{team}'")
    elif oord == 'd':
        new_df = df.query(f"eventType == '{event}' and shotClock_x == 24.0 and PLAYER1_TEAM_NICKNAME == '{team}'")
    else:
        new_df = df.query(f"eventType == '{event}' and PLAYER1_TEAM_NICKNAME == '{team}'")
    
    new_coords = pd.DataFrame(new_df.pop('ball').tolist(), index=new_df.index, columns = ['x','y','z'])
    combined = pd.concat([new_df, new_coords.reindex(new_df.index)], axis=1).dropna()

    return combined.drop(columns=['gameId'])

game_ids = ['0042100301', '0042100302', '0042100303', '0042100304', '0042100305', '0042100306', '0042100307',\
            '0042100311', '0042100312', '0042100313', '0042100314', '0042100315', '0042100401', '0042100402',\
            '0042100403', '0042100404', '0042100405', '0042100406']