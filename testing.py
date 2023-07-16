import data

game2 = data.load_game("0042100302")
print(game2)
evs = game2.eventType.unique().tolist()
game2_oreb = data.game_evs(game2, evs.index('REB'), 'o')
game2_dreb = data.game_evs(game2, evs.index('REB'), 'd')
print(game2_oreb)
print(game2_dreb)