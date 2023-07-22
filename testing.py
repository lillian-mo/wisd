import data
# import matplotlib.pylot as plt

from matplotlib import pyplot

import numpy as np


game2 = data.load_game("0042100302")
twoand3 = data.mult_games(['0042100302', '0042100303'])
evs = game2.eventType.unique().tolist()
tos = data.game_evs(twoand3, 'TO')
game2_oreb = data.game_evs(game2, 'REB', 'o')
game2_dreb = data.game_evs(game2, 'REB', 'd')
orebs_team1 = game2_oreb.query("((period == 1 | period == 2) and x < 0.00) | ((period == 3 | period == 4) and x > 0.0)")

## get coords within bounds 
orebs_team1_xy = orebs_team1.filter(['x', 'y']).query('x <= 47 and x >= -47')
orebs_team1_x = orebs_team1_xy.filter(['x']) # x-coords
orebs_team1_y = orebs_team1_xy.filter(['y']) # y-coords

## load court image
img = pyplot.imread("bigcourt.jpg")
pyplot.imshow(img, extent=[-47, 47, -25, 25]) ## show image

## plot coords in a scatter plot
pyplot.scatter(orebs_team1_x, orebs_team1_y)

## set axes scale
pyplot.xticks([-47, 0, 47])
pyplot.yticks([-25, 0, 25])

## label axes & title
pyplot.xlabel('x', weight='bold')
pyplot.ylabel('y', weight='bold', rotation=0)
pyplot.title('Density Map (NBA)', weight='bold')

pyplot.show()