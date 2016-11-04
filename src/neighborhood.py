import math

def gaussian(d, sigma):
    p = math.pow(sigma,2)
    if p == 0:
        return 0
    return math.exp(-d/(2*p))
