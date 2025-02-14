import numpy as np

def logistic_map(x, r=3.99, n=1000):
    """ Generate chaotic sequence using logistic map """
    sequence = []
    for _ in range(n):
        x = r * x * (1 - x)
        sequence.append(x)
    return np.argsort(sequence)

def scramble_pixels(data):
    """ Apply chaotic scrambling to DNA sequence """
    key = logistic_map(0.5, n=len(data))
    return np.array(list(data))[key]

def unscramble_pixels(data):
    """ Unscramble chaotic DNA sequence """
    key = logistic_map(0.5, n=len(data))
    unscrambled = np.empty_like(data)
    unscrambled[key] = np.array(list(data))
    return unscrambled
