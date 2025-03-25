import numpy as np

# Simple DNA Encoding/Decoding with fixed rule set for stability
DNA_ENCODING = {
    "00": "A", "01": "T", "10": "C", "11": "G"
}

# DNA Decoding Table
DNA_DECODING = {v: k for k, v in DNA_ENCODING.items()}

def image_to_dna(image):
    """ Convert image to DNA sequence """
    binary_data = np.unpackbits(image)  # Convert to binary
    binary_str = "".join(map(str, binary_data))

    dna_sequence = "".join(DNA_ENCODING[binary_str[i:i+2]] for i in range(0, len(binary_str), 2))
    
    return dna_sequence, image.shape

def dna_to_image(dna_sequence, shape):
    """ Convert DNA sequence back to image """
    binary_str = "".join(DNA_DECODING[nucleotide] for nucleotide in dna_sequence)
    
    binary_array = np.array(list(map(int, binary_str)), dtype=np.uint8)
    
    expected_size = np.prod(shape) * 8  # Expected bits
    if len(binary_array) != expected_size:
        # Handle size mismatch
        if len(binary_array) < expected_size:
            # Pad with zeros
            padding = np.zeros(expected_size - len(binary_array), dtype=np.uint8)
            binary_array = np.concatenate([binary_array, padding])
        else:
            # Truncate
            binary_array = binary_array[:expected_size]

    image = np.packbits(binary_array)  # Convert back to bytes
    return image.reshape(shape)

# If module is run directly, print out encoding table
if __name__ == "__main__":
    print("[ℹ] Using fixed DNA encoding scheme:")
    for binary, nucleotide in DNA_ENCODING.items():
        print(f"  {binary} -> {nucleotide}")