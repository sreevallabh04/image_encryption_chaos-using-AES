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
    seed = 0.5  # Fixed seed for consistency
    key = logistic_map(seed, n=len(data))
    return np.array(list(data))[key]

def unscramble_pixels(data):
    """ Unscramble chaotic DNA sequence """
    seed = 0.5  # Same fixed seed as scrambling
    key = logistic_map(seed, n=len(data))
    
    # Convert to array of characters if input is a string
    if isinstance(data, str):
        data_array = np.array(list(data))
    else:
        data_array = np.array(list(data))
    
    # Apply unscrambling
    unscrambled = np.empty_like(data_array)
    unscrambled[key] = data_array
    
    # Return in original format
    if isinstance(data, str):
        return ''.join(unscrambled)
    else:
        return unscrambled

# If module is run directly, demonstrate chaotic sequence
if __name__ == "__main__":
    # Generate a small chaotic sequence for demonstration
    seed = 0.5
    sequence = logistic_map(seed, r=3.99, n=20)
    print("[ℹ] Chaotic sequence example (first 20 values):")
    print(sequence)