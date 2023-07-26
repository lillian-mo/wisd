import data
import math
import matplotlib.pyplot as plt
import matplotlib as mpl

# game ids
game_ids = ['0042100301', '0042100302', '0042100303', '0042100304', '0042100305', '0042100306', '0042100307',\
            '0042100311', '0042100312', '0042100313', '0042100314', '0042100315', '0042100401', '0042100402',\
            '0042100403', '0042100404', '0042100405', '0042100406']

## Heat Offensive Rebounds (Game 1)
game1 = data.load_game(game_ids[0]) # load in game
game1_reb = data.game_evs(game1, 4, 'Heat', 'd') # get defensive rebounds 
game1_shots = data.game_evs(game1, [1, 2], 'Heat') # get shots
danger_lvl = data.high_danger(game1_reb, game1_shots).filter(['danger'])['danger'].values.tolist() # get list of danger values

## Heat Offensive Rebounds (All games)
# all_games = data.mult_games(game_ids)
# all_games_reb = data.game_evs(all_games, 4, 'Heat', ['o', 'd'])

## bounds of the court & net location
court_x = 47
court_y = 25


def get_coords(game, axis):
    lop = []
    if axis == 'x':
        for point in game: lop.append(point[0])
    else:
        for point in game: lop.append(point[1])
    return lop


def label_points(game, labels):
    game_x = get_coords(game, 'x')
    game_y = get_coords(game, 'y')

    ## display danger levels of points to the net
    for i in range(len(game_x)):
        plt.text(game_x[i], game_y[i], labels[i], size = 5)
        

def plot_init(game, team):
    game1_dreb = game.query('x >= -47 and x <= 47').filter(['x', 'y']).values.tolist()
    # shot_xy = [[0, -15], [0, -10], [0, -5], [0, 0], [0, 5], [0, 10], [0, 15], [0, 20]] # location of shots (sample)

    ## load court image as background
    img = plt.imread("..\wisd\court.jpg")
    plt.imshow(img, extent=[-court_x, court_x, -court_y, court_y]) ## show image

    ## set axes scale
    plt.xticks([-court_x, 0, court_x])
    plt.yticks([-court_y, 0, court_y])

    ## label axes & title
    plt.xlabel('x', weight='bold')
    plt.ylabel('y', weight='bold', rotation=0)
    plt.title('Rebounds ({})'.format(team), weight='bold')

    ## create colour map
    c = danger_lvl

    ## custom colourmaps
    if team == 'Heat':
        # custom_cmap = mpl.colors.LinearSegmentedColormap.from_list('custom', ['orange', 'maroon', 'black']) # gradient
        custom_cmap = mpl.colors.ListedColormap(['orange', 'maroon', 'black'])

    elif team == 'Celtics':
        custom_cmap =  mpl.colors.ListedColormap(['tan', 'green', 'black'])

    ## plot locations of shots
    # plt.scatter(get_coords(shot_xy, 'x'), get_coords(shot_xy, 'y'), alpha = 0.3, s = 50)

    ## plot points of defensive rebounds
    plt.scatter(get_coords(game1_dreb, 'x'), get_coords(game1_dreb, 'y'), \
                c = c, cmap = custom_cmap, alpha = 0.75, s = 50)

    # for i in range(len(shot_xy)):
    #     plt.plot([get_coords(shot_xy, 'x')[i], get_coords(game1_oreb_r, 'x')[i]], \
    #              [get_coords(shot_xy, 'y')[i], get_coords(game1_oreb_r, 'y')[i]], \
    #              'red', linestyle = 'dashed', linewidth = 1, alpha = 0.3)

    plt.clim(3, 5)
    cbar = plt.colorbar(ticks = [3, 4, 5], orientation = 'vertical', shrink = 0.5)
    cbar.set_ticklabels(['low', 'medium', 'high'], size = 5)
    cbar.set_label(label = 'Danger Level', size = 8)


plot_init(game1_reb, 'Heat') # plot the points
plt.show() # display the scatter plot