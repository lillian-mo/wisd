import pandas as pd
import json


with open ('./metadata/games.json', 'r') as f:
    games = json.load(f)

with open('./metadata/teams.json', 'r') as f:
    teams = json.load(f)

team_meta = pd.read_json(json.dumps(teams['teams']))
game_meta = pd.read_json(json.dumps(games['games']))


game_meta['nbaId'] = game_meta['nbaId'].astype(int)
all_games = game_meta[(game_meta['nbaId'] >= 42100301) & (game_meta['nbaId'] <= 42100406)]
all_games['homeTeamId'] = all_games['homeTeamId'].map(team_meta.set_index('id')['name'])
all_games['awayTeamId'] = all_games['awayTeamId'].map(team_meta.set_index('id')['name'])
all_games = all_games.filter(items=['id', 'homeTeamId', 'awayTeamId', 'nbaId'])
all_games = all_games.rename(columns={'id': 'game', 'homeTeamId': 'homeTeam', 'awayTeamId': 'awayTeam'})