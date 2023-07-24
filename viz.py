import data
import math
import matplotlib.pyplot as plt

# game ids
game_ids = ['0042100301', '0042100302', '0042100303', '0042100304', '0042100305', '0042100306', '0042100307',\
            '0042100311', '0042100312', '0042100313', '0042100314', '0042100315', '0042100401', '0042100402',\
            '0042100403', '0042100404', '0042100405', '0042100406']

## Heat Offensive Rebounds (Game 1)
game1 = data.load_game(game_ids[0])
game1_oreb = data.game_evs(game1, 4, 'Heat', 'o')

## Heat Offensive Rebounds (All games)
# mult_games = data.mult_games(game_ids)
# mult_games_oreb = data.game_evs(mult_games, 4, 'Heat', 'o')

## bounds of the court & net location
court_x = 47
court_y = 25
net_l = [-42.1, 0.2]
net_r = [41.9, 0.2]


def get_dist(lorb):
    lod = []
    if lorb[0][0] < 0: ## left half of court
        for point in lorb: lod.append(math.hypot(point[0] - net_l[0], point[1] - net_l[1]))
    else:
        for point in lorb: lod.append(math.hypot(point[0] - net_r[0], point[1] - net_r[1]))
    return lod


def get_coords(game, axis):
    lop = []
    if axis == 'x':
        for point in game: lop.append(point[0])
    else:
        for point in game: lop.append(point[1])
    return lop


def label_points(game):
    game_x = get_coords(game, 'x')
    game_y = get_coords(game, 'y')

    ## display distance of points to the net
    for i in range(len(game_x)):
        plt.text(game_x[i], game_y[i], game_y[i], size = 5)
        

def plot_init(game, team):
    game1_oreb_l = game.query('x < 0').filter(['x', 'y']).values.tolist()
    game1_oreb_r = game.query('x > 0').filter(['x', 'y']).values.tolist()

    ## load court image as background
    img = plt.imread("..\wisd\court.jpg")
    plt.imshow(img, extent=[-court_x, court_x, -court_y, court_y]) ## show image

    ## set axes scale
    plt.xticks([-court_x, 0, court_x])
    plt.yticks([-court_y, 0, court_y])

    ## label axes & title
    plt.xlabel('x', weight='bold')
    plt.ylabel('y', weight='bold', rotation=0)
    plt.title('Offensive Rebounds ({})'.format(team), weight='bold')

    ## create colour map
    c1 = get_dist(game1_oreb_l)
    c2 = get_dist(game1_oreb_r)

    ## plot points & colour bar
    plt.scatter(get_coords(game1_oreb_l, 'x'), get_coords(game1_oreb_l, 'y'), \
                c = c1, cmap = 'autumn', alpha = 0.75)
    plt.scatter(get_coords(game1_oreb_r, 'x'), get_coords(game1_oreb_r, 'y'), \
                c = c2, cmap = 'autumn', alpha = 0.75)
    plt.clim(0, max(c1 + c2))
    cbar = plt.colorbar(orientation = 'vertical', shrink = 0.5)
    cbar.set_label(label = 'Distance', size = 8)


plot_init(game1_oreb, 'Heat') # plot the points
plt.show() # display the scatter plot