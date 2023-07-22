import pandas as pd
import json


with open ('./metadata/games.json', 'r') as f:
    games = f.readlines()

with open('./metadata/teams.json', 'r') as f:
    teams = f.readlines()

games_meta = pd.read_json('./metadata/games.json')
teams_meta = pd.read_json('./metadata/teams.json')

print(games_meta)
print(teams_meta)