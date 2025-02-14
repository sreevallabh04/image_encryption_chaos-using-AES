import cv2
import numpy as np
from dna_crypto import image_to_dna
from hybrid_crypto import encrypt_dna
from chaos import scramble_pixels
import os

# Load image
image_path = "images/input.jpg"
image = cv2.imread(image_path)

# Convert image to DNA sequence
dna_sequence, original_shape = image_to_dna(image)

# Encrypt DNA sequence
encrypted_dna = encrypt_dna(dna_sequence)

# Apply chaotic scrambling
scrambled_dna = scramble_pixels(encrypted_dna)

# Save encrypted data
np.save("images/encrypted.npy", scrambled_dna)
np.save("images/original_shape.npy", original_shape)

print("[✔] Image Encrypted Successfully!")
