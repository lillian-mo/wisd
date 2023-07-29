import data
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib as mpl

# game ids
game_ids = ['0042100301', '0042100302', '0042100303', '0042100304', '0042100305', '0042100306', '0042100307',\
            '0042100311', '0042100312', '0042100313', '0042100314', '0042100315', '0042100401', '0042100402',\
            '0042100403', '0042100404', '0042100405', '0042100406']

## Team Defensive Rebounds (All games)
danger_df, danger_df_l, danger_df_r = data.get_dangers(game_ids, 'Mavericks')
danger_l = danger_df_l.dropna().filter(['danger'])['danger'].values.tolist()
danger_r = danger_df_r.dropna().filter(['danger'])['danger'].values.tolist()

## bounds of court
court_x = 47
court_y = 25


def get_coords(lst):
    x, y = [], []

    for point in lst: 
        x.append(point[0]) # add x coords from lst
        y.append(point[1]) # add y coords from lst
    return x, y


def label_points(game, labels):
    x, y = get_coords(game)

    ## display danger levels of points to the net
    for i in range(len(x)):
        plt.text(x[i], y[i], labels[i], size = 5)
    

def get_colours(team):
    ## custom colourmaps
    if team == 'Heat':
        colours = mpl.colors.ListedColormap(['#f9a01b', '#98002e', '#000000'])
    elif team == 'Celtics':
        colours =  mpl.colors.ListedColormap(['#bc9a5c', '#008853', '#000000'])
    elif team == 'Warriors':
        colours = mpl.colors.ListedColormap(['#ffc72c', '#006bb6', '#0b385f'])
    elif team == 'Mavericks':
        colours = mpl.colors.ListedColormap(['#c4ced4', '#1061ac', '#000000'])
    return colours


def plot_init(games, team):
    dreb_x, dreb_y = get_coords(games.filter(['x', 'y']).values.tolist()) # x,y coords of def rebs
    danger = games.filter(['danger'])['danger'].values.tolist()
    
    ## load court image as background
    img = plt.imread("..\wisd\court.jpg")
    plt.imshow(img, extent=[-court_x, court_x, -court_y, court_y]) # show image

    ## set axes scale
    plt.xticks([-court_x, 0, court_x])
    plt.yticks([-court_y, 0, court_y])

    ## label axes & title
    plt.xlabel('x', weight='bold')
    plt.ylabel('y', weight='bold', rotation=0)
    plt.title('Defensive Rebounds ({})'.format(team), weight='bold')

    ## set colour and set size scaling
    c = danger
    s = [point**3 for point in danger]

    plt.scatter(dreb_x, dreb_y, c = c, cmap = get_colours(team), alpha = 0.75, s = 75) # plot def rebs

    ## create colour bar
    plt.clim(3, 5)
    cbar = plt.colorbar(ticks = [3, 4, 5], orientation = 'vertical', shrink = 0.5)
    cbar.set_ticklabels(['low', 'medium', 'high'], size = 5)
    cbar.set_label(label = 'Danger Level', size = 8)


def plot_conv_init(games, team):
    shot_x, shot_y = get_coords(games.dropna().filter(['shot_x', 'shot_y']).values.tolist()) # x,y coords of shots
    shot_dreb_x, shot_dreb_y = get_coords(games.dropna().filter(['x', 'y']).values.tolist()) # x,y coords of rebounds resulting in shots
    danger = games.dropna().filter(['danger'])['danger'].values.tolist()

    ## load court image as background
    img = plt.imread("..\wisd\court.jpg")
    plt.imshow(img, extent=[-court_x, court_x, -court_y, court_y]) # show image

    ## set axes scale
    plt.xticks([-court_x, 0, court_x])
    plt.yticks([-court_y, 0, court_y])

    ## label axes & title
    plt.xlabel('x', weight='bold')
    plt.ylabel('y', weight='bold', rotation=0)
    plt.title('Defensive Rebounds Conversion ({})'.format(team), weight='bold')

    ## set colour and set size scaling
    c = danger
    s = [point**3 for point in danger] 

    ## plot locations of shots & connection of rebounds to corresponding shots
    shot_plot = plt.scatter(shot_x, shot_y, marker = 'X', s = 45)

    for i in range(len(shot_x)):
        plt.plot([shot_x[i], shot_dreb_x[i]], [shot_y[i], shot_dreb_y[i]], \
                'grey', linestyle = 'dashed', linewidth = 1, alpha = 0.75)
        
    line_plot = mlines.Line2D([], [], color = 'grey', linestyle = 'dashed') # dashed line to rep rebound connections in legend
    plt.legend((shot_plot, line_plot), ['shots', 'rebounds to shots'], loc = 0, fontsize = 7) # legend

    plt.scatter(shot_dreb_x, shot_dreb_y, c = c, cmap = get_colours(team), alpha = 0.75, s = s) # plot def rebs leading to shots

    ## create colour bar
    plt.clim(3, 5)
    cbar = plt.colorbar(ticks = [3, 4, 5], orientation = 'vertical', shrink = 0.5)
    cbar.set_ticklabels(['low', 'medium', 'high'], size = 5)
    cbar.set_label(label = 'Danger Level', size = 8)


plot_init(danger_df, 'Mavericks') # plot defensive rebounds
# plot_conv_init(danger_df_l, 'Mavericks') # plot defensive rebound conversion left half
# plot_conv_init(danger_df_r, 'Mavericks') # plot defensive rebound conversion right half

plt.show() # display the scatter plot