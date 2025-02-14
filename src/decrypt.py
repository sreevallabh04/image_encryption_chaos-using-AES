import cv2
import numpy as np
from dna_crypto import dna_to_image
from hybrid_crypto import decrypt_dna
from chaos import unscramble_pixels

# Load encrypted data
scrambled_dna = np.load("images/encrypted.npy", allow_pickle=True)
original_shape = np.load("images/original_shape.npy", allow_pickle=True)

# Apply chaotic unscrambling
unscrambled_dna = unscramble_pixels(scrambled_dna)

# Decrypt DNA sequence
decrypted_dna = decrypt_dna(unscrambled_dna)

# Convert DNA back to image
decrypted_image = dna_to_image(decrypted_dna, original_shape)

# Save decrypted image
cv2.imwrite("images/decrypted.png", decrypted_image)

print("[✔] Image Decrypted Successfully & Stored in 'images/decrypted.png'")
