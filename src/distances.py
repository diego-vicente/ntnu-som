import math


def manhattan_distance_2d(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def euclidean_distance_2d(x, y):
    return math.sqrt(pow(y[0]-x[0],2) + pow(y[1]-x[1],2))


def euclidean_distance_1d(x, y):
    return abs(x-y)


def euclidean_distance_1d_circular(n, i, j):
    """
    Calculates 1d distance of integers i and j in a circle of n elements.
    :param n: Circle length
    :param i: Start element
    :param j: Target element
    :return: Minimal distance
    """
    d = euclidean_distance_1d(i, j)
    return min(d, n-d)
