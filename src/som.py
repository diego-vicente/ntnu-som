from helper import read_data, plot_map
import random

def main():
    cities = read_data('western_sahara')
    run_som(cities, 100000, 0.2)

def run_som(cities, iterations, learning_rate):
    # Initialize the weights of the neurons
    neurons = [[11000, 24000]]
    for i in range(1, len(cities) * 4):
        neurons.append([neurons[i-1][0] + 10,
                        neurons[i-1][1] + 10])

    for i in range(iterations):
        # Pick a random city
        city = random.choice(cities)
        # Choose the winner neuron
        winner, winner_index = choose_winner(city, neurons)
        # Update the weights of the neuron and its neighbourhood
        for j in range(-3, 3):
            k = winner_index + j
            if 0 <= k < len(neurons):
                neighbour = abs(1 / j*2) if j != 0 else 0.7
                neurons[k][0] += learning_rate * neighbour * (city[0] - neurons[k][0])
                neurons[k][1] += learning_rate * neighbour * (city[1] - neurons[k][1])

        if i % 10000 == 0:
            plot_map(cities, neurons, i)

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


if __name__ == '__main__': main()
