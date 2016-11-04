#!/usr/bin/env python3

from decay import StaticDecay, LinearDecay, ExponentialDecay
from helper import read_data, plot_map
from neighborhood import gaussian
import random
from operator import itemgetter
from functools import partial
import math

def main():
    cities = read_data('western_sahara')
    cities = normalize(cities)

    neuron_count = len(cities) * 4
    radius = ExponentialDecay(neuron_count/10, 0.95)
    learning_rate = ExponentialDecay(0.8, 0.9999)
    neurons = init_neurons(neuron_count)

    som(neurons, cities, 500, gaussian, learning_rate, radius)


def init_neurons(count):
    """
    Initialize the weights of the neurons
    """
    return [[random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)] for i in range(count)]


def som(neurons, cities, iterations, neighborhood, learning_rate, radius):
    for i in range(iterations):
        # Pick a random city
        city = cities[i % len(cities)]
        # Choose the winner neuron
        winner, winner_index = choose_winner(city, neurons)

        distance = partial(list_euclidian_distance, len(neurons))

        # Update the weights of the neuron and its neighbourhood
        for neuron_index, neuron in enumerate(neurons):
            d = distance(neuron_index, winner_index)
            nf = neighborhood(d, radius.value)
            neuron[0] += learning_rate.value * nf * (city[0] - neuron[0])
            neuron[1] += learning_rate.value * nf * (city[1] - neuron[1])

        if i < 250 and i % 5 == 0:
            plot_map(cities, neurons, i)

        learning_rate.decay()
        radius.decay()

    plot_map(cities, neurons, iterations)

def manhattan_distance(center, neuron):
    return abs(center[0] - neuron[0]) + abs(center[1] - neuron[1])

def choose_winner(city, neurons):
    minimum = 1000000
    index = 0
    for i in range(len(neurons)):
        distance = manhattan_distance(city, neurons[i])
        if distance < minimum:
            winner = neurons[i]
            minimum = distance
            index = i
    return winner, index


def normalize(cities):
    """
    Normalize list of city coordinates
    :param cities: list of tuples, containing x and y coordinate
    :return: normalized list of city coordinates
    """
    max_x = max(cities,key=itemgetter(0))[0]
    max_y = max(cities,key=itemgetter(1))[1]

    return [(x/max_x, y/max_y) for (x, y) in cities]


def list_euclidian_distance(n, i, j):
    if(j<i):
        t = j
        j = i
        i = t
    if j-i <= n/2:
        return j-i
    return i - (j-n)

if __name__ == '__main__': main()
