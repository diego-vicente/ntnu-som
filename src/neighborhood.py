import math


def gaussian(d, sigma):
    p = sigma**2
    if p == 0:
        return 0
    return math.exp(-d**2/(2*p))


def bubble(d, sigma):
    if d <= sigma:
        return 1
    return 0
