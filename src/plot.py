import matplotlib.pyplot as plt

def plot_map(cities, neurons, iteration):
    """
    Generates the required map of cities and neurons at a given moment and
    stores the result in a png image. The map contains all the cities
    represented as red dots and all the neurons as green, crossed by a line
    dots. The method plots the iteration in which the snapshot was taken.
    :param cities: the cities to be plotted, passed as a list of (x, y)
    coordinates
    """
    plt.scatter(*zip(*cities), color='red')
    plt.scatter(*zip(*neurons), color='green')

    plt.plot(*zip(*neurons), color='darkgreen')

    plt.title('Iteration #{:06d}'.format(iteration))
    plt.axis('off')
    plt.savefig('{:06d}.png'.format(iteration))
