import numpy as np

def logistic_map(seed, length):
    """Generates a chaotic sequence using the logistic map."""
    x = seed
    r = 3.99  # Chaotic range (3.57 - 4)
    sequence = []
    
    for _ in range(length):
        x = r * x * (1 - x)  # Logistic map equation
        sequence.append(int(x * 255) % 256)  # Normalize to byte range
    
    return bytes(sequence)

def generate_chaotic_key():
    """Generates a 16-byte AES key using the chaotic logistic map."""
    seed = np.random.rand()  # Random seed between 0 and 1
    return logistic_map(seed, 16)

if __name__ == "__main__":
    key = generate_chaotic_key()
    print("Generated Chaotic Key:", key.hex())
