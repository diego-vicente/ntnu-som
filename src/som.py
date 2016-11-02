from helper import read_data, plot_map
import random

def main():
    cities = read_data('western_sahara')
    run_som(cities, 20, 0.2)

def run_som(cities, iterations, learning_rate):
    # Initialize the weights of the neurons
    neurons = []
    for i in range(len(cities)):
        neurons.append([random.randint(9700, 12700),
                        random.randint(20833, 27470)])
    for i in range(iterations):
        # Pick a random city
        city = random.choice(cities)
        # Choose the winner neuron
        winner = choose_winner(city, neurons)
        # Update the weights of the neuron and its neighbourhood
        for neuron in neurons:
            neighbour = 1 / (manhattan_distance(winner, neuron) + 2)
            neuron[0] += learning_rate * neighbour * (city[0] - winner[0])
            neuron[1] += learning_rate * neighbour * (city[1] - winner[0])

        plot_map(cities, neurons, i)

    plot_map(cities, neurons, iterations)


def manhattan_distance(center, neuron):
    return abs(center[0] - neuron[0]) + abs(center[1] - neuron[1])

def choose_winner(city, neurons):
    minimum = 1000000
    for neuron in neurons:
        distance = manhattan_distance(city, neuron)
        if distance < minimum:
            winner = neuron
            minimum = distance
    return winner


if __name__ == '__main__': main()
