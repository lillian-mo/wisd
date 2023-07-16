import data

game2 = data.load_game("0042100302")
twoand3 = data.mult_games(['0042100302', '0042100303'])
evs = game2.eventType.unique().tolist()
orebs = data.game_evs(twoand3, 'TO')
game2_oreb = data.game_evs(game2, 'REB', 'o')
game2_dreb = data.game_evs(game2, 'REB', 'd')
print(orebs)
print(game2_oreb)
print(game2_dreb)