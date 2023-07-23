import data
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

game2 = data.load_game("0042100302")
twoand3 = data.mult_games(['0042100302', '0042100303'])

evs = game2.eventType.unique().tolist()
tos = data.game_evs(twoand3, 'REB', 'o')
game2_oreb = data.game_evs(game2, 'REB', 'o')
game2_dreb = data.game_evs(game2, 'REB', 'd')
orebs_team1 = tos.query("((period == 1 | period == 2) and x < 0.00) | ((period == 3 | period == 4) and x > 0.0)")

## bounds of the court
court_x = 47
court_y = 25


## get coords within bounds 
def get_game_xy(game, axis):
    return game.query('x <= 47 and x >= -47').filter([axis])[axis].values.tolist() 


net_l = [-42.1, 0.2]
net_r = [41.9, 0.2]

orebs_team1_l = orebs_team1.query('x < 0').filter(['x', 'y']).values.tolist()
orebs_team1_r = orebs_team1.query('x > 0').filter(['x', 'y']).values.tolist()

def get_dist(lorb):
    lodist = []
    for point in lorb:
        lodist.append(math.hypot(point[0] - net_l[0]))





## calculate kernal density
def game_kde(game_x, game_y):
    ## convert points into a numpy array
    x = np.array(game_x)
    y = np.array(game_y)
    xy = np.vstack([x, y]) # arrange arrays vertically to form a single array
    return gaussian_kde(xy)(xy) # return point density


def plot_init(x, y):
    ## load court image as background
    img = plt.imread("..\wisd\court.jpg")
    plt.imshow(img, extent=[-court_x, court_x, -court_y, court_y]) ## show image

    ## set axes scale
    plt.xticks([-court_x, 0, court_x])
    plt.yticks([-court_y, 0, court_y])

    ## label axes & title
    plt.xlabel('x', weight='bold')
    plt.ylabel('y', weight='bold', rotation=0)
    plt.title('Density Map (NBA)', weight='bold')

    ## plot points & colourmap
    c = game_kde(x, y)
    plt.scatter(x, y, c = c, cmap = 'hot_r', alpha = 0.75)
    cbar = plt.colorbar(orientation = 'vertical', shrink = 0.5)
    cbar.set_label(label = 'Density', size = 8)


plot_init(get_game_xy(orebs_team1, 'x'), get_game_xy(orebs_team1, 'y')) # plot the points
plt.show() # display the scatter plot