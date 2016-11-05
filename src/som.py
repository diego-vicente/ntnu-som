#!/usr/bin/env python3

from helper import read_data, plot_map, get_input
from neighborhood import gaussian, bubble
from distances import euclidean_distance
import random
from operator import itemgetter
from functools import partial


def main():
    data_set, n_neurons, iterations, learning_rate, radius = get_input()
    cities = read_data(data_set)
    scaling, cities = normalize(cities)

    neuron_count = len(cities) * n_neurons
    neurons = init_neurons(neuron_count)

    som(neurons, cities, iterations, gaussian, learning_rate, radius, scaling)


def init_neurons(count):
    """
    Initialize the weights of the neurons
    """
    return [[random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)] for i in range(count)]


def som(neurons, cities, iterations, neighborhood, learning_rate, radius, scaling):
    for i in range(iterations):
        # Pick a random city
        city = cities[i % len(cities)]
        # Choose the winner neuron
        winner_index, winner = compute_winner(city, neurons, euclidean_distance)

        distance = partial(list_euclidian_distance, len(neurons))

        if i < iterations and i % 50 == 0:
            plot_map(cities, neurons, i)
            print("TSP distance: ", calculate_tsp(cities, neurons)*scaling)

        # Update the weights of the neuron and its neighbourhood
        for neuron_index, neuron in enumerate(neurons):
            d = distance(neuron_index, winner_index)
            nf = neighborhood(d, radius.value)
            neuron[0] += learning_rate.value * nf * (city[0] - neuron[0])
            neuron[1] += learning_rate.value * nf * (city[1] - neuron[1])

        learning_rate.decay()
        radius.decay()

    plot_map(cities, neurons, iterations)


def compute_winner(city, neurons, distance):
    return min([(i, distance(city, neuron)) for i, neuron in enumerate(neurons)], key=itemgetter(1))


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


def list_euclidian_distance(n, i, j):
    if(j<i):
        t = j
        j = i
        i = t
    if j-i <= n/2:
        return j-i
    return i - (j-n)


def calculate_tsp(cities, neurons):

    city_neurons = {}
    for city_idx, city in enumerate(cities):
        # find nearest neuron
        idx, _ = compute_winner(city, neurons, euclidean_distance)
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
    tsp_distance = euclidean_distance(tsp_order[0], tsp_order[-1])
    for idx in range(len(tsp_order)-1):
        tsp_distance += euclidean_distance(tsp_order[idx], tsp_order[idx+1])

    return tsp_distance

if __name__ == '__main__': main()
