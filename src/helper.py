import matplotlib.pyplot as plt
import os
from decay import StaticDecay, LinearDecay, ExponentialDecay
from neighborhood import gaussian, bubble

DEFAULTS_EXP = {'uruguay': ('uruguay', 8, 10000, 1000, 500, bubble,
                        ExponentialDecay(0.7, 0.9999),
                        ExponentialDecay(734*8/10, 0.999)),
            'western_sahara': ('western_sahara', 8, 500, 50, 50, gaussian,
                        ExponentialDecay(0.7, 0.999),
                        ExponentialDecay(29*8/10, 0.995)),
            'qatar': ('qatar', 8, 5000, 500, 500, gaussian,
                        ExponentialDecay(0.9, 0.9999),
                        ExponentialDecay(194*8/10, 0.997)),
            'djibouti': ('djibouti', 8, 1000, 50, 50, gaussian,
                        ExponentialDecay(0.7, 0.999),
                        ExponentialDecay(89*8/10, 0.995))}

DEFAULTS_LIN = {'uruguay': ('uruguay', 8, 10000, 1000, 500, gaussian,
                        LinearDecay(0.9, 0.000089),
                        LinearDecay(734*8/10, 0.055)),
            'western_sahara': ('western_sahara', 8, 500, 50, 50, gaussian,
                        LinearDecay(0.7, 0.001),
                        LinearDecay(29*8/10, 0.04)),
            'qatar': ('qatar', 8, 10000, 500, 500, gaussian,
                        LinearDecay(0.7, 0.000065),
                        LinearDecay(194*8/10, 0.015)),
            'djibouti': ('djibouti', 8, 5000, 50, 50, gaussian,
                        LinearDecay(0.7, 0.0001),
                        LinearDecay(89*8/10, 0.014))}

DEFAULT_STA = {'uruguay': ('uruguay', 8, 10000, 1000, 200, gaussian,
                        StaticDecay(0.4),
                        StaticDecay(500)),
            'western_sahara': ('western_sahara', 6, 5000, 1000, 200, gaussian,
                        StaticDecay(0.3),
                        StaticDecay(5)),
            'qatar': ('qatar', 6, 5000, 1000, 200, gaussian,
                        StaticDecay(0.4),
                        StaticDecay(50)),
            'djibouti': ('djibouti', 4, 5000, 1000, 200, gaussian,
                        StaticDecay(0.2),
                        StaticDecay(10))}

plt.figure()


def plot_map(cities, neurons, iteration):
    """
    Generates the required map of cities and neurons at a given moment and
    stores the result in a png image. The map contains all the cities
    represented as red dots and all the neurons as green, crossed by a line
    dots. The method plots the iteration in which the snapshot was taken.
    :param cities: the cities to be plotted, passed as a list of (x, y)
    coordinates
    :param neurons: the cities to be plotted, passed as a list of (x, y)
    coordinates
    :param iteration: the iterations when the snapshot is taken
    :return: returns nothing
    """
    plt.scatter(*zip(*cities), color='red', s=3)
    plt.scatter(*zip(*neurons), color='green', s=2)

    plt.plot(*zip(*(neurons+[neurons[0]])), color='darkgreen')

    # Invert x axis to match representation at
    # http://www.math.uwaterloo.ca/tsp/world/countries.html
    plt.gca().invert_xaxis()
    plt.gca().set_aspect('equal', adjustable='datalim')

    plt.title('Iteration #{:06d}'.format(iteration))
    plt.axis('off')
    plt.savefig('results/{}.png'.format(iteration))
    plt.clf()


def read_data(filename):
    """
    Reads and parses data from a txt file with a map data. The format that the
    function expects is the one followed in the uwaterloo TSP web archive
    (math.uwaterloo.ca/tsp/world/countries.html), ignoring the first
    description lines that have to be manually removed. The method searches for
    the filename in the assets folder.
    :param filename: the path to the file to be parsed
    :return: the cities as a list of (x, y) coordinates
    """
    cities = []

    path = 'assets/{}.txt'.format(filename)
    with open(path, 'r') as f:
        for line in f:
            city = list(map(float, line.split()[1:]))
            cities.append((city[1], city[0]))

    return cities


def get_input():
    """
    Gets the input from the user line or launches the default values
    :return data_set: list of cities as (x,y) coordinates
    :return n_neurons: number of neurons per city in the data_set
    :return iterations: number of iterations to be executed
    :return learning_rate: learning rate to be used
    :return radius: radius of neurons to be used
    """
    data_sets = {'w': 'western_sahara', 'q': 'qatar', 'u': 'uruguay',
                 'd': 'djibouti'}

    set_id = input('Data set [w/q/u/d]: ') or 'w'
    data_set = data_sets[set_id]

    if not os.path.isfile('assets/{}.txt'.format(data_set)):
        exit("Did not find this data set file!")

    use_defaults = input('Do you want to use default parameters? (y/n) ') == 'y'

    if use_defaults:
        decay = input('What kind of decay? [s/l/e]') or 'e'
        if decay == 'e':
            return DEFAULTS_EXP[data_set]
        if decay == 'l':
            return DEFAULTS_LIN[data_set]
        if decay == 's':
            return DEFAULT_STA[data_set]
    # Comprehensive input
    n_neurons = int(input('How many neurons per city? (8)') or 8)
    iterations = int(input('How many iterations (500)?') or 500)
    learning_rate = get_input_decay('learning rate')
    radius = get_input_decay('radius')
    k = int(input('After how many iterations print current TSP distance? (1000)') or 1000)
    plot_k = int(input('After how many iterations generate plot? (200)') or 200)

    neighborhood = input('Choose neighborhood function: [g/b]') or 'b'
    if neighborhood == 'b':
        neighborhood = bubble
    elif neighborhood == 'g':
        neighborhood = gaussian
    else:
        exit('Not a valid neighborhood!')

    return data_set, n_neurons, iterations, k, plot_k, neighborhood, learning_rate, radius

def get_input_decay(name):
    """
    Generates the appropriate decay function for a given variable. The decays
    that can be generated are static (no decay over time), linear and
    exponential.
    :param name: name of the variable that will be generated
    :return: decay function for the variable with appropriate parameters
    """
    decay = input('What kind of decay for {}? [s/l/e]'.format(name)) or 'e'
    if decay == 's':
        value = float(input('Static value: '))
        return StaticDecay(value)
    if decay == 'l':
        value = float(input('Start value: '))
        rate = float(input('Rate:'))
        return LinearDecay(value, rate)
    if decay == 'e':
        value = float(input('Start value: '))
        rate = float(input('Rate:'))
        return ExponentialDecay(value, rate)
    exit('Not a valid option!')
