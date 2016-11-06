#!/usr/bin/env python3

from helper import read_data, plot_map, get_input
from neighborhood import gaussian, bubble
from distances import euclidean_distance_2d, euclidean_distance_1d_circular

import random
from operator import itemgetter
from functools import partial


def main():
    data_set, n_neurons, iterations, learning_rate, radius = get_input()
    cities = read_data(data_set)
    scaling, cities = normalize(cities)

    neuron_count = len(cities) * n_neurons
    neurons = init_neurons(neuron_count)

    # TODO get user input for k = 50 and neighborhood function, distance
    som(neurons, cities, iterations, 1000, 200, bubble, learning_rate, radius,
        scaling)


def init_neurons(count):
    """
    Initialize the weights of the neurons
    :param count: number of neurons to initialize
    :return: list of neurons as weight vectors (x,y)
    """
    return [[random.uniform(0.0, 1.0),
             random.uniform(0.0, 1.0)] for i in range(count)]


def som(neurons, cities, iterations, k, plot_k, neighborhood, learning_rate,
        radius, scaling):
    """
    Main SOM loop to be executed.
    :param neurons: list of neurons as weight vectors (x,y)
    :param cities: list of cities as (x,y) coordinates
    :param iterations: number of iterations to perform
    :param k: lapse of iterations between printing execution data
    :param plot_k: lapse of iterations between saving the map images
    :param neighborhood: type of neighborhood to use in the execution
    :param learning_rate: learning rate to be used
    :param radius: radius of neurons to be used
    :param scaling: scale used when normalizing the data
    :return: returns nothing
    """
    for i in range(0, iterations+1):
        if i % k == 0:
            print('#', i, '\t\tTSP-distance: ',
                  calculate_tsp(cities, neurons)*scaling)
        if i % plot_k == 0:
            plot_map(cities, neurons, i)
        if i == iterations:
            break
        som_iteration(neurons, cities, neighborhood, learning_rate, radius)


def som_iteration(neurons, cities, neighborhood, learning_rate, radius):
    """
    Performs a single SOM iteration with a given set of parameters
    :param neurons: list of neurons as weight vectors (x,y)
    :param cities: list of cities as (x,y) coordinates
    :param neighborhood: type of neighborhood to use in the execution
    :param learning_rate: learning rate to be used
    :param radius: radius of neurons to be used
    :return: returns nothing
    """
    # Pick a random city
    city = cities[random.randint(0, len(cities)-1)]
    # Choose the winner neuron
    winner_index, winner = compute_winner(city, neurons, euclidean_distance_2d)
    distance = partial(euclidean_distance_1d_circular, len(neurons))

    # Update the weights of the neuron and its neighbourhood
    for neuron_index, neuron in enumerate(neurons):
        d = distance(neuron_index, winner_index)
        nf = neighborhood(d, radius.value)
        neuron[0] += learning_rate.value * nf * (city[0] - neuron[0])
        neuron[1] += learning_rate.value * nf * (city[1] - neuron[1])

    learning_rate.decay()
    radius.decay()


def compute_winner(city, neurons, distance):
    """
    Computes the closest neuron to a given city with a given distance
    :param city: coordinates (x,y) of the city to be associated to the winner
    :param neurons: list of neurons as weight vectors (x,y)
    :param distance: type of distance to be used for the computations
    :return winner_index: index of the chosen neuron in the neuron list
    :return winner: closest neuron to city
    """
    return min([(i, distance(city, neuron)) for i,
                neuron in enumerate(neurons)], key=itemgetter(1))


def normalize(cities):
    """
    Normalize list of city coordinates
    :param cities: list of tuples, containing x and y coordinate
    :return: normalized list of city coordinates
    """
    max_x = max(cities,key=itemgetter(0))[0]
    max_y = max(cities,key=itemgetter(1))[1]
    m = max(max_x, max_y)

    return m, [(x/m, y/m) for (x, y) in cities]


def calculate_tsp(cities, neurons):
    """
    Computes the Travelling Salesman distance to travel all the cities using a
    list of neurons
    :param cities: list of tuples, containing x and y coordinate
    :param neurons: list of neurons as weight vectors (x,y)
    :return: the distance to travel through cities using neurons
    """
    city_neurons = {}
    for city_idx, city in enumerate(cities):
        # find nearest neuron
        idx, _ = compute_winner(city, neurons, euclidean_distance_2d)
        if idx not in city_neurons:
            city_neurons[idx] = [city]
        else:
            city_neurons[idx].append(city)

    # order cities according to neuron order
    tsp_order = []
    for neuron_idx in range(len(neurons)):
        if neuron_idx in city_neurons:
            tsp_order += city_neurons[neuron_idx]

    # calculate tsp distance for tsp_order
    tsp_distance = euclidean_distance_2d(tsp_order[0], tsp_order[-1])
    for idx in range(len(tsp_order)-1):
        tsp_distance += euclidean_distance_2d(tsp_order[idx],
                                              tsp_order[idx + 1])

    return tsp_distance


if __name__ == '__main__': main()
