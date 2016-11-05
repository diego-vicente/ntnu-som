import math


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def euclidean_distance(x, y):
    return math.sqrt(pow(y[0]-x[0],2) + pow(y[1]-x[1],2))