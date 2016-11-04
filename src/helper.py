import matplotlib.pyplot as plt

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
    plt.figure()
    plt.scatter(*zip(*cities), color='red', s = 3)
    plt.scatter(*zip(*neurons), color='green', s = 2)

    plt.plot(*zip(*(neurons+[neurons[0]])), color='darkgreen')

    plt.title('Iteration #{:06d}'.format(iteration))
    plt.axis('off')
    plt.savefig('results/{}.png'.format(iteration))

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
