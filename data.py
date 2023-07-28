# This file contains all the functions that filter through the dataframes 
# for rebounds and correspoding high danger chances

import pandas as pd
from pandas import DataFrame
from py_ball import playbyplay
from typing import Union

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

# EVENTMSGTYPE code from pbp data with corresponding eventType data
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

# the EVENTMSGCODE for the event, along with the danger level it corresponds to
danger_type = {
    0: 3,
    1: 5,
    2: 4
} 

def load_game(game_id: str) -> DataFrame:
    """a function that creates a merged dataframe of relevant data from events, tracking, and pbp for a given game

    Args:
        game_id (str): the id of the game being called

    Returns:
        DataFrame: a dataframe merging the events, tracking, and pbp from the corresponding game
    """
    # this reads the events, tracking, and play dataframes separately
    df_e = pd.read_json(f"./games/{game_id}/{game_id}_events.jsonl", lines=True)
    df_t = pd.read_json(f"./games/{game_id}/{game_id}_tracking.jsonl", lines=True).drop_duplicates(subset=['gameClock','period'])
    plays = playbyplay.PlayByPlay(headers=HEADERS,
                              endpoint='playbyplayv2',
                              game_id=game_id)
    play_df = pd.DataFrame(plays.data['PlayByPlay'])
    play_df = play_df.filter(items=['EVENTNUM', 'EVENTMSGTYPE', 'GAME_ID', 'PLAYER1_TEAM_NICKNAME'])
    play_df['event'] = play_df['EVENTMSGTYPE'].map(event_dict)

    # merges events and tracking based on gameClock and period
    e_and_t = df_e.merge(df_t, how='inner', on=['gameClock', 'period']).filter\
                    (items=['gameId', 'eventType','shotClock_x','gameClock','period','ball', 'pbpId'])

    # merges events and tracking with the pbp data
    final_df = e_and_t.merge(play_df, left_on=['eventType','pbpId'], right_on=['event','EVENTNUM'], how='inner').\
                    rename(columns={'PLAYER1_TEAM_NICKNAME': 'team'}).drop(columns=['event', 'pbpId'])
       
    return final_df


def mult_games(games: list) -> DataFrame:
    """loads multiple games

    Args:
        games (list): the list of game ids

    Returns:
        DataFrame: the dataframe (following the format from load_game) with data from the games in the list
    """
    df = load_game(games[0])
    for i in games[1:]:
        df = pd.concat(objs=[df, load_game(i)], ignore_index=True)

    return df

def game_evs(df: DataFrame, events: Union[list, int], team: str='none', oord: str='none') -> DataFrame:
    """filters the dataframe based on the event(s)

    Args:
        df (DataFrame): the game(s) data
        events (Union[list, int]): either a list of the event codes or an event code
        team (str, optional): the team that performed the event. Defaults to 'none'.
        oord (str, optional): if the event is a rebound, whether it's offensive('o') or defensive('d'). Defaults to 'none'.

    Returns:
        DataFrame: a dataframe with the games filtered on event
    """

    new_df = df
    new_df['rebmatch'] = new_df.team.eq(new_df.team.shift())

    # queries by offensive or defensive, if given
    if oord == 'o':
        new_df = new_df.query(f"rebmatch == True")
    if oord == 'd':
        new_df = new_df.query(f"rebmatch == False")

    # queries by event
    if type(events) == list:
        string = f"EVENTMSGTYPE == {events[0]}"
        for i in events:
            string = f"{string} or EVENTMSGTYPE == {i}"
        new_df = new_df.query(string)
    else:
        new_df = new_df.query(f"EVENTMSGTYPE == {events}")

    # queries by team, if given
    if team != 'none':
        new_df = new_df.query(f"team == '{team}'") 

    # separates the ball
    new_coords = pd.DataFrame(new_df.pop('ball').tolist(), index=new_df.index, columns = ['x','y','z'])
    combined = pd.concat([new_df, new_coords.reindex(new_df.index)], axis=1).dropna().drop(columns=['rebmatch', 'z'])

    return combined.drop(columns=['gameId'])

def in_ranges(time: float, period: int, game: int, team: str, ranges: list) -> Union[bool, list]:
    """determines whether or not a given shot was taken in a 10 second part of the game

    Args:
        time (float): the time on the game clock when the shot happened
        period (int): the period that it happened in
        game (int): the game it was in
        team (str): the team that made the shot
        ranges (list): a list of potential 10 second parts

    Returns:
        Union[bool, list]: the first element of the list says if the shot happened while the second returns the 
                           rebound time it was attached to if it happened, and False if it didn't
    """
    time_int = int(time * 100)
    for i in ranges:
        if time_int >= i[0] and time_int <= i[1] and period == i[2] and game == i[3] and team == i[4]:
            return [True, i[1]]
    
    return [False, False]


def high_danger(rebs: DataFrame, shots: DataFrame) -> DataFrame:
    """_summary_

    Args:
        rebs (DataFrame): the dataframe of rebounds
        shots (DataFrame): the dataframe of shots

    Returns:
        DataFrame: the dataframe of rebounds in addition to columns with the shot that came in transition if there was one, 
                   along with danger level
    """

    # creates the list of 10-sec ranges post defensive rebound
    reb_ranges = []
    n = rebs.gameClock.values.tolist()
    p = rebs.period.values.tolist()
    g = rebs.GAME_ID.values.tolist()
    t = rebs.team.values.tolist()
    for i in range(len(n)- 1):
        num = n[i]
        reb_ranges.append([int(num * 100) - 1000, int(num * 100), p[i], int(g[i]), t[i]])
    
    # checks if the shots are in range
    shots['inRange'] = shots.apply(lambda x: in_ranges(x.gameClock, x.period, int(x.GAME_ID), x.team, reb_ranges), axis=1)
    range_pop = pd.DataFrame(shots.pop('inRange').tolist(), index=shots.index, columns=['bool', 'time'])
    shots_new = pd.concat([shots, range_pop.reindex(shots.index)], axis=1).\
                drop(columns=['EVENTNUM', 'shotClock_x', 'eventType']).\
                rename(columns={'EVENTMSGTYPE': 'shotType', 'x': 'shot_x', 'y': 'shot_y'})
    
    rebs.loc[:, 'int_time'] = (rebs['gameClock'] * 100).astype(int)

    # combines the rebounds with their respective shots, if a shot exists
    together = pd.merge(rebs, shots_new, left_on=['int_time', 'period', 'GAME_ID', 'team'], right_on=['time', 'period', 'GAME_ID', 'team'], how='left')
    together['shotType'] = together['shotType'].fillna(0).astype(int)
    together['danger'] = together['shotType'].map(danger_type)
    together = together.drop(columns=['shotClock_x', 'EVENTMSGTYPE', 'int_time', 'shotType', 'bool', 'time'])

    return together.drop_duplicates(subset='gameClock_x', keep='first')

def get_dangers(games: list, team: str):
    game_df = mult_games(games)

    rebound_df = game_evs(game_df, 4, team, 'd').query('x >= -47 and x <= 47')
    rebound_l = rebound_df.query('x <= 0')
    rebound_r = rebound_df.query('x > 0')

    shot_df = game_evs(game_df, [1, 2], team)

    danger = high_danger(rebound_df, shot_df)
    danger_l = high_danger(rebound_l, shot_df)
    danger_r = high_danger(rebound_r, shot_df)

    return danger, danger_l, danger_r