import data

game2 = data.load_game("0042100302")
twoand3 = data.mult_games(['0042100302', '0042100303'])
evs = game2.eventType.unique().tolist()
tos = data.game_evs(twoand3, 'TO')
game2_oreb = data.game_evs(game2, 'REB', 'o')
game2_dreb = data.game_evs(game2, 'REB', 'd')
orebs_team1 = game2_oreb.query("((period == 1 | period == 2) and x < 0.00) | ((period == 3 | period == 4) and x > 0.0)")
print(orebs_team1)

orebs_team1.to_csv('team 1_oreb.csv')